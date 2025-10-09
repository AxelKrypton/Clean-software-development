using DelimitedFiles, DataFrames

function filterInvalidRows!(df)
	# Remove any rows with non-numeric, missing, NaN, or nothing values in any column
	filter!(row -> all(x -> (isa(x, Number) && !isinf(x) && !isnan(x) && !ismissing(x) && !isnothing(x)), row), df)
	# Remove duplicate rows
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

pathEggwin = "../../Ising2D/Eggwin/Ising_2D_MCMC_Ns8_Ns8/"
pathBeaktrix = "../../Ising2D/Beaktrix/ising2d_L16"
pathSiegfried = "../../Ising2D/Siegfried/two_dimensional_ising_model_markov_chain_monte_carlo_Sz32/"

Eggwin_df = readEggwinFile(pathEggwin)
Beaktrix_df = readBeaktrixFile(pathBeaktrix)
Siegfried_df = readSiegfriedFile(pathSiegfried)

# Combine all DataFrames
combined_df = vcat(Eggwin_df, Beaktrix_df, Siegfried_df)

#TODO: Check that the combined dataframe fulfills alls requirements (only numeric values, no NaN, no Inf, no missing, no nothing, no duplicates, e in [-1, 1], abs_m in [0, 1] etc.)