using DelimitedFiles, DataFrames

<<<<<<< HEAD
pathEggwin = "../../Ising2D/Eggwin/Ising_2D_MCMC_Ns8_Ns8/"
pathBeaktrix = "../../Ising2D/Beaktrix/ising2d_L16"
pathSiegfried = "../../Ising2D/Siegfried/two_dimensional_ising_model_markov_chain_monte_carlo_Sz32/"
=======
pathEggwin = "./Ising2D/Eggwin/Ising_2D_MCMC_Ns8_Ns8/"
>>>>>>> 563d32cddd3c7511daaa144ba075507ef53f57c0

function readEggwinFile(path::String)
	files = readdir(path)

	df_list = DataFrame[]

	for file in files
		data, header = readdlm(joinpath(path, file), header = true);
		df = DataFrame(data[:, 1:3], ["Configuration", "M", "E"])

		L = 8
		V = L*L
		T = parse(Float64, split(split(file, "temp")[2], ".txt")[1])

		df[!, "T"] .= T
		df[!, "L"] .= L

		# Remove any rows with missing, NaN, or nothing values in any column
		filter!(row -> all(x -> (isa(x, Number) && !isinf(x) && !isnan(x) && !ismissing(x) && !isnothing(x)), row), df)

		# Normalization
		df[!, "e"] .= - df[!, "E"] ./ (4*V)
		df[!, "abs_m"] .= abs.(df[!, "M"] ./ V)

		#drop columns E and M
		select!(df, Not(["E", "M"]))

<<<<<<< HEAD
		# Remove rows where "e" is larger than 1 or smaller than 0
		filter!(row -> (-1 .<= row.e .<= 1), df)
		filter!(row -> (0 .<= row.abs_m .<= 1), df)

		# Check for duplicates within the file
		unique!(df)
=======
        filterDataframe(df)
>>>>>>> 563d32cddd3c7511daaa144ba075507ef53f57c0

		push!(df_list, df)
	end

   

	# Concatenate all DataFrames in the list into a single DataFrame
	df = reduce(vcat, df_list)
    # Remove duplicate rows
    unique!(df)

	# Check for duplicates between files
	unique!(df)

	# Sort by temperature 
	sort!(df, [:T])


	return df
end

<<<<<<< HEAD
=======
 #Assuming DF already in common format
 function filterDataframe(df)
    # Remove any rows with missing, NaN, or nothing values in any column
    filter!(row -> all(x -> !(isnan(x) && ismissing(x) && isnothing(x)), row), df)

    # Remove rows where "e" is larger than 1 or smaller than 0
    filter!(row -> (-1 .<= row.e .<= 1), df)
    filter!(row -> (0 .<= row.abs_m .<= 1), df)

end
>>>>>>> 563d32cddd3c7511daaa144ba075507ef53f57c0


function readBeaktrixFile(path::String)
	files = readdir(path)

	df_list = DataFrame[]

	for file in files
		data = readdlm(joinpath(path, file));
		df = DataFrame(data[:, 1:3], ["Configuration", "E", "M"])

		L = 16
		V = L*L
		T = parse(Float64, split(split(file, "T")[2], ".txt")[1])

		# Remove any rows with missing, NaN, or nothing values in any column
		filter!(row -> all(x -> (isa(x, Number) && !isinf(x) && !isnan(x) && !ismissing(x) && !isnothing(x)), row), df)


		df[!, "T"] .= T
		df[!, "L"] .= L

		# Normalization
		df[!, "e"] .= df[!, "E"] ./ 4
		df[!, "abs_m"] .= abs.(df[!, "M"] ./ 1)

		#drop columns E and M
		select!(df, Not(["E", "M"]))

		# Remove rows where "e" is larger than 1 or smaller than 0
		filter!(row -> (-1 .<= row.e .<= 1), df)
		filter!(row -> (0 .<= row.abs_m .<= 1), df)

		unique!(df)

		push!(df_list, df)
	end

	# Concatenate all DataFrames in the list into a single DataFrame
	df = reduce(vcat, df_list)

	unique!(df)

	# Sort by temperature 
	sort!(df, [:T])


	return df
end

<<<<<<< HEAD
function readSiegfriedFile(path::String)
	files = readdir(path)

	df_list = DataFrame[]

	for file in files
		data = readdlm(joinpath(path, file));
		df = DataFrame(data[:, 1:4], ["T", "Configuration", "E", "M"])

		L = 32
		V = L*L
		T = parse(Float64, split(split(file, "T")[2], ".txt")[1])

		if !all(df.T .== T)
			@warn "Temperature in filename $(file) does not match temperature in file. Continuing with temperature $(df.T[1]) from file instead."
			T = df.T[1]
			@assert all(df.T .== T) "Not all temperatures in file $(file) are the same."
		end


		# Remove any rows with missing, NaN, or nothing values in any column
		filter!(row -> all(x -> (isa(x, Number) && !isinf(x) && !isnan(x) && !ismissing(x) && !isnothing(x)), row), df)

		# Drop the existing T column and replace it with the parsed temperature to have the column in the correct position for consistency
		select!(df, Not(["T"]))
		df[!, "T"] .= T

		df[!, "L"] .= L

		# Normalization
		df[!, "e"] .= -df[!, "E"] ./ 4
		df[!, "abs_m"] .= abs.(df[!, "M"] ./ 1)

		#drop columns E and M
		select!(df, Not(["E", "M"]))

		# Remove rows where "e" is larger than 1 or smaller than 0
		filter!(row -> (-1 .<= row.e .<= 1), df)
		filter!(row -> (0 .<= row.abs_m .<= 1), df)

		unique!(df)

		push!(df_list, df)
	end

	# Concatenate all DataFrames in the list into a single DataFrame
	df = reduce(vcat, df_list)

	unique!(df)

	# Sort by temperature 
	sort!(df, [:T])


	return df
end

=======
Eggwin_df = readEggwinFile(pathEggwin)
>>>>>>> 563d32cddd3c7511daaa144ba075507ef53f57c0
