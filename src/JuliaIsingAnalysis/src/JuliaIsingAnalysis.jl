using DelimitedFiles, DataFrames

pathEggwin = "../../Ising2D/Eggwin/Ising_2D_MCMC_Ns8_Ns8/"

function readEggwinFile(path::String)
	files = readdir(path)

	df_list = DataFrame[]

	for file in files
		data, header = readdlm(joinpath(path, file), header = true);
		df = DataFrame(data[:, 1:3], ["Configuration", "M", "E"])

		V = 8*8
		T = parse(Float64, split(split(file, "temp")[2], ".txt")[1])

		df[!, "T"] .= T
		df[!, "V"] .= V

		# Normalization
		df[!, "e"] .= df[!, "E"] ./ (4*V)
		df[!, "abs_m"] .= abs.(df[!, "M"] ./ V)

		#drop columns E and M
		select!(df, Not(["E", "M"]))


		# Remove any rows with missing, NaN, or nothing values in any column
		filter!(row -> all(x -> !(isnan(x) && ismissing(x) && isnothing(x)), row), df)

		# Remove rows where "e" is larger than 1 or smaller than 0
		filter!(row -> (-1 .<= row.e .<= 1), df)
		filter!(row -> (0 .<= row.abs_m .<= 1), df)

		# Remove duplicate rows
		unique!(df)

		push!(df_list, df)
	end

	# Concatenate all DataFrames in the list into a single DataFrame
	df = reduce(vcat, df_list)

	# Sort by temperature 
	sort!(df, [:T])


	return df
end

function readBeaktrixFile(path::String)
end
# module JuliaIsingAnalysis
