module JuliaIsingAnalysis

using DelimitedFiles
using DataFrames
using CairoMakie
using Statistics

export main, readEggwinFile, readBeaktrixFile, readSiegfriedFile, createPlots, computeChiAndBinder, bootstrap, PATH_TO_BEAKTRIX_DATA, PATH_TO_EGGWIN_DATA, PATH_TO_SIEGFRIED_DATA

const PATH_TO_DATA_DIRECTORY = joinpath(@__DIR__, "..", "..", "..", "Ising2D")
const PATH_TO_EGGWIN_DATA = joinpath(PATH_TO_DATA_DIRECTORY, "Eggwin", "Ising_2D_MCMC_Ns8_Ns8")
const PATH_TO_BEAKTRIX_DATA = joinpath(PATH_TO_DATA_DIRECTORY, "Beaktrix", "ising2d_L16")
const PATH_TO_SIEGFRIED_DATA = joinpath(PATH_TO_DATA_DIRECTORY, "Siegfried", "two_dimensional_ising_model_markov_chain_monte_carlo_Sz32")

"""
Removes any duplicate rows and rows with non-numeric data (including NaN, Inf, missing, nothing) from the given DataFrame.
"""
function filterInvalidRows!(df::DataFrame)
	filter!(row -> all(x -> (isa(x, Number) && !isinf(x) && !isnan(x) && !ismissing(x) && !isnothing(x)), row), df)
	unique!(df)
end

# Assuming DF already in common format
function filterInvalidPhysics!(df)
	# Remove rows where "e" is larger than 1 or smaller than 0
	filter!(row -> (-1 .<= row.e .<= 1), df)
	filter!(row -> (0 .<= row.abs_m .<= 1), df)
end

function readEggwinFile(path::String)
	files = readdir(path)

	df_list = DataFrame[]

	for file in files
		data, _ = readdlm(joinpath(path, file), header = true);
		df = DataFrame(data[:, 1:3], ["Configuration", "M", "E"])

		L = 8
		T = parse(Float64, split(split(file, "temp")[2], ".txt")[1])

		df[!, "T"] .= T
		df[!, "L"] .= L

		filterInvalidRows!(df)

		# Check that Configuration number can be converted to integer
		@assert all(isinteger.(df.Configuration)) "Configuration number in file $(file) contains non-integer values."
		# Convert Configuration number from float to integer
		df[!, :Configuration] = convert.(Int64, df[!, :Configuration])

		# Normalization
		V = L*L
		df[!, "e"] .= - df[!, "E"] ./ (4*V)
		df[!, "abs_m"] .= abs.(df[!, "M"] ./ V)
		select!(df, Not(["E", "M"]))

		filterInvalidPhysics!(df)

		push!(df_list, df)
	end

	# Concatenate all DataFrames in the list into a single DataFrame
	df = reduce(vcat, df_list)

	# Check for duplicates between files
	unique!(df)

	# Sort by temperature 
	sort!(df, [:T])

	return df
end

function readBeaktrixFile(path::String)
	files = readdir(path)

	df_list = DataFrame[]

	for file in files
		data = readdlm(joinpath(path, file));
		df = DataFrame(data[:, 1:3], ["Configuration", "E", "M"])

		L = 16
		T = parse(Float64, split(split(file, "T")[2], ".txt")[1])

		df[!, "T"] .= T
		df[!, "L"] .= L

		filterInvalidRows!(df)

		# Check that Configuration number can be converted to integer
		@assert all(isinteger.(df.Configuration)) "Configuration number in file $(file) contains non-integer values."
		# Convert Configuration number from float to integer
		df[!, :Configuration] = convert.(Int64, df[!, :Configuration])

		# Normalization
		df[!, "e"] .= df[!, "E"] ./ 4
		df[!, "abs_m"] .= abs.(df[!, "M"] ./ 1)
		select!(df, Not(["E", "M"]))

		filterInvalidPhysics!(df)

		push!(df_list, df)
	end

	# Concatenate all DataFrames in the list into a single DataFrame
	df = reduce(vcat, df_list)

	# Check for duplicates between files
	unique!(df)

	# Sort by temperature 
	sort!(df, [:T])

	return df
end

function readSiegfriedFile(path::String)
	files = readdir(path)

	df_list = DataFrame[]

	for file in files
		data = readdlm(joinpath(path, file));
		df = DataFrame(data[:, 1:4], ["T", "Configuration", "E", "M"])

		L = 32
		T = parse(Float64, split(split(file, "T")[2], ".txt")[1])

		if !all(df.T .== T)
			@warn "Temperature in filename $(file) does not match temperature in file. Continuing with temperature $(df.T[1]) from file instead."
			T = df.T[1]
			@assert all(df.T .== T) "Not all temperatures in file $(file) are the same."
		end
		# Drop the existing T column and replace it with the parsed temperature to have the column in the correct position for consistency
		select!(df, Not(["T"]))
		df[!, "T"] .= T
		df[!, "L"] .= L

		filterInvalidRows!(df)

		# Check that Configuration number can be converted to integer
		@assert all(isinteger.(df.Configuration)) "Configuration number in file $(file) contains non-integer values."
		# Convert Configuration number from float to integer
		df[!, :Configuration] = convert.(Int64, df[!, :Configuration])

		# Normalization
		df[!, "e"] .= -df[!, "E"] ./ 4
		df[!, "abs_m"] .= abs.(df[!, "M"] ./ 1)
		select!(df, Not(["E", "M"])) # Drop columns E and M after normalization

		filterInvalidPhysics!(df)

		push!(df_list, df)
	end

	# Concatenate all DataFrames in the list into a single DataFrame
	df = reduce(vcat, df_list)

	# Check for duplicates between files
	unique!(df)

	# Sort by temperature 
	sort!(df, [:T])

	return df
end

function bootstrap(df, n_resamples::Int)
	n = nrow(df)

	resample_energies = Float64[]
	resample_magnetizations = Float64[]
	resample_chis = Float64[]
	resample_binders = Float64[]

	for _ in 1:n_resamples
		resample_indices = rand(1:n, n)  # Sample with replacement
		resample = df[resample_indices, :]

		push!(resample_energies, mean(resample.e))
		push!(resample_magnetizations, mean(resample.abs_m))

		chi, binder = computeChiAndBinder(resample)
		push!(resample_chis, chi)
		push!(resample_binders, binder)
	end

	return mean(resample_energies), std(resample_energies), mean(resample_magnetizations), std(resample_magnetizations), mean(resample_chis), std(resample_chis), mean(resample_binders), std(resample_binders)
end

function computeChiAndBinder(df)
	@assert all(df.T .== df.T[1]) "All temperature values in the dataframe must be the same to compute susceptibility."
	@assert all(df.L .== df.L[1]) "All L values in the dataframe must be the same to compute susceptibility."

	T = df.T[1]
	V = df.L[1]^2

	mean_m = mean(df.abs_m)
	mean_m2 = mean(df.abs_m .^ 2)

	chi = V/T * (mean_m2 - mean_m^2)

	mean_m4 = mean(df.abs_m .^ 4)
	B = 1 - (mean_m4 / (3 * mean_m2^2))

	return chi, B
end

function createPlots(df)
	fig1 = Figure()
	ax1 = Axis(fig1[1, 1], xlabel = "Temperature T", ylabel = "Energy per spin e", title = "Energy per spin vs Temperature")

	fig2 = Figure()
	ax2 = Axis(fig2[1, 1], xlabel = "Temperature T", ylabel = "Absolute value of Magnetization per spin |m|", title = "Magnetization per spin vs Temperature")

	fig3 = Figure()
	ax3 = Axis(fig3[1, 1], xlabel = "Temperature T", ylabel = "Susceptibility χ", title = "Susceptibility vs Temperature")

	fig4 = Figure()
	ax4 = Axis(fig4[1, 1], xlabel = "Temperature T", ylabel = "Binder Cumulant B", title = "Binder Cumulant vs Temperature")

	fig5 = Figure()
	ax5 = Axis(fig5[1, 1], xlabel = "Temperature T", ylabel = "Binder Cumulant Ratios B(L)/B(2 L)", title = "Binder Cumulant Ratios vs Temperature")

	gdf = groupby(df, :L)
	for subdf in gdf
		# perform bootstrap for each temperature
		subdf_grouped_by_temperature = groupby(subdf, :T)

		T = Float64[]
		mean_energy = Float64[]
		std_energy = Float64[]

		mean_magnetization = Float64[]
		std_magnetization = Float64[]

		mean_chis = Float64[]
		std_chis = Float64[]

		mean_binders = Float64[]
		std_binders = Float64[]

		for subsubdf in subdf_grouped_by_temperature
			mean_e, std_e, mean_m, std_m, mean_chi, std_chi, mean_binder, std_binder = bootstrap(subsubdf, 1000)

			push!(T, subsubdf.T[1])

			push!(mean_energy, mean_e)
			push!(std_energy, std_e)

			push!(mean_magnetization, mean_m)
			push!(std_magnetization, std_m)

			push!(mean_chis, mean_chi)
			push!(std_chis, std_chi)

			push!(mean_binders, mean_binder)
			push!(std_binders, std_binder)
		end


		lines!(ax1, T, mean_energy; label = "L = $(subdf.L[1])")
		errorbars!(ax1, T, mean_energy, std_energy, whiskerwidth = 5)

		lines!(ax2, T, mean_magnetization; label = "L = $(subdf.L[1])")
		errorbars!(ax2, T, mean_magnetization, std_magnetization, whiskerwidth = 5)

		lines!(ax3, T, mean_chis; label = "L = $(subdf.L[1])")
		errorbars!(ax3, T, mean_chis, std_chis, whiskerwidth = 5)

		lines!(ax4, T, mean_binders; label = "L = $(subdf.L[1])")
		errorbars!(ax4, T, mean_binders, std_binders, whiskerwidth = 5)
	end

	axislegend(ax1; position = :rb)
	axislegend(ax2; position = :rt)
	axislegend(ax3; position = :rt)
	axislegend(ax4; position = :rt)

	# Add vertical line at critical temperature
	vlines!.([ax1, ax2, ax3, ax4], [2/log(1+sqrt(2))], color = :red, linestyle = :dash)

	display(fig1)
	save("avg_energy_vs_temperature.pdf", fig1)

	display(fig2)
	save("avg_magnetization_vs_temperature.pdf", fig2)

	display(fig3)
	save("susceptibility_vs_temperature.pdf", fig3)

	display(fig4)
	save("binder_cumulant_vs_temperature.pdf", fig4)

	return nothing
end

function main()
	Eggwin_df = readEggwinFile(PATH_TO_EGGWIN_DATA)
	Beaktrix_df = readBeaktrixFile(PATH_TO_BEAKTRIX_DATA)
	Siegfried_df = readSiegfriedFile(PATH_TO_SIEGFRIED_DATA)

	combined_df = vcat(Eggwin_df, Beaktrix_df, Siegfried_df)
	unique!(combined_df) # Ensure no duplicates between datasets

	createPlots(combined_df)
end

@static if (abspath(PROGRAM_FILE) == @__FILE__)
	main()
end


end



