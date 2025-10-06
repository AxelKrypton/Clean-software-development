module Powerweek

using ArgParse # Command line parsing
using HDF5 # Reading and writing data
using Glob # File path expansion
using DataFrames # Data structures
using DataFrames: outerjoin, ncol
using ProgressBars
using Statistics
using StatsBase

function parse_commandline()
	s = ArgParseSettings()

	@add_arg_table! s begin
		"--base-path", "-i"
		help = "Path where the input data directory is located"
		arg_type = String
		default = "./data"

		"--output-path", "-o"
		help = "Path where the output directory is located"
		arg_type = String
		default = nothing # If not specified, the output path will be set to base_path/averaged
	end

	return parse_args(s)
end

const args = parse_commandline()
const base_path = args["base-path"]
const output_path = eval(args["output-path"] === nothing ? joinpath(base_path, "averaged") : args["output-path"])

"""
	Recursively searches for files matching the given pattern `pattern_string` in the specified directory `dir`.
	Returns a nested list of file paths that match the pattern.
"""
function rdir(dir::AbstractString, pattern_string::AbstractString)
	@assert isdir(dir) "The specified path $dir does not exist or is not a directory."
	@assert !isempty(pattern_string) "The pattern string cannot be empty."
	pattern = Glob.FilenameMatch(pattern_string)
	result = []
	for (root, _, files) in walkdir(dir)
		file_paths = filter!(f -> occursin(pattern, f), joinpath.(root, files))
		if !isempty(file_paths)
			push!(result, file_paths)
		end
	end
	return result
end

"""
	Reads all HDF5 files in the given list of file paths `files` and returns a single DataFrame containing all the data.
"""
function readfiles(files::Vector{String})
	numfiles = length(files)
	original_data = DataFrame()

	#error handling if number of files is larger than 99999
	@assert numfiles > 0 "No files found in $path"
	@assert numfiles < 99999 "Number of files is larger than 99999. Exiting."

	# Read the first file to get the time t and external field J columns.
	@debug "Reading file $(files[1])"
	original_data[!, :t] = Float64.(h5read(files[1], "data/t"))
	original_data[!, :J] = Float64.(h5read(files[1], "data/J"))
	@assert !isempty(original_data.t) "Time column is empty in $(files[1])"
	@assert !any(isnan.(original_data.t)) "Time column contains NaN in $(files[1])"
	@assert !isempty(original_data.J) "External field column is empty in $(files[1])"
	@assert !any(isnan.(original_data.J)) "External field column contains NaN in $(files[1])"

	T = h5readattr(files[1], "data")["T"]
	N = h5readattr(files[1], "data")["N"]
	mSq = h5readattr(files[1], "data")["mSq"]
	gamma = h5readattr(files[1], "data")["gamma"]
	D = h5readattr(files[1], "data")["D"]
	lambda = h5readattr(files[1], "data")["lambda"]
	precision = h5readattr(files[1], "data")["precision"]

	for i in ProgressBar(1:numfiles, unit = "files", printing_delay = 1)  # Loop over all files in the folder
		@debug "Reading file $(files[i])"

		# Check that the parameters are identical for all files
		@assert h5readattr(files[i], "data")["T"] == T "Temperature mismatch in $(files[i])"
		@assert h5readattr(files[i], "data")["N"] == N "Lattice size mismatch in $(files[i])"
		@assert h5readattr(files[i], "data")["mSq"] == mSq "Mass squared mismatch in $(files[i])"
		@assert h5readattr(files[i], "data")["gamma"] == gamma "Gamma mismatch in $(files[i])"
		@assert h5readattr(files[i], "data")["D"] == D "Dimension mismatch in $(files[i])"
		@assert h5readattr(files[i], "data")["lambda"] == lambda "Lambda mismatch in $(files[i])"
		@assert h5readattr(files[i], "data")["precision"] == precision "Precision mismatch in $(files[i])"
		@assert h5read(files[i], "data/t") == original_data.t "Time column mismatch in $(files[i])"
		@assert h5read(files[i], "data/J") == original_data.J "External field column mismatch in $(files[i])"

		original_data[!, Symbol("M_$i")] = Float64.(h5read(files[i], "data/M"))

		@assert !isempty(original_data[!, Symbol("M_$i")]) "Magnetization column is empty in $(files[i])"
		@assert !any(isnan.(original_data[!, Symbol("M_$i")])) "Magnetization column contains NaN in $(files[i])"
	end

	# center time around J(t=0) =0
	original_data.t .-= original_data.t[end] / 2

	J_delta = abs(original_data.J[end] - original_data.J[1])
	t_delta = abs(original_data.t[end] - original_data.t[1])

	attributes = Dict(
		"J_delta" => J_delta,
		"t_delta" => t_delta,
		"T" => T,
		"N" => N,
		"mSq" => mSq,
		"gamma" => gamma,
		"D" => D,
		"lambda" => lambda,
		"n" => numfiles,
	)

	return original_data, attributes
end

function bootstrap_observables(original_sample, attributes)
	@debug "Generating bootstrap sample"
	nrows = nrow(original_sample)
	sample_size = ncol(original_sample)
	sample_cols = StatsBase.sample(1:sample_size, sample_size, replace = true)

	M = zeros(Float64, nrows)
	M_abs = zeros(Float64, nrows)
	M² = zeros(Float64, nrows)
	M³ = zeros(Float64, nrows)
	M⁴ = zeros(Float64, nrows)

	for col in sample_cols
		M .+= original_sample[!, col]
		M_abs .+= abs.(original_sample[!, col])
		M² .+= original_sample[!, col] .^ 2
		M³ .+= original_sample[!, col] .^ 3
		M⁴ .+= original_sample[!, col] .^ 4
	end

	M ./= sample_size
	M_abs ./= sample_size
	M² ./= sample_size
	M³ ./= sample_size
	M⁴ ./= sample_size

	T = attributes["T"] # Temperature
	V = attributes["N"]^attributes["D"] # Volume of the system

	χ = (M² .- M .^ 2) .* (V / T)
	κ3 = (M³ .- 3 .* M² .* M .+ 2 .* M .^ 3) .* (V / T) .^ 2
	κ4 = (M⁴ .- 4 .* M³ .* M .- 3 .* M² .^ 2 .+ 12 .* M² .* M .^ 2 .- 6 .* M .^ 4) .* (V / T) .^ 3

	return M, M_abs, χ, κ3, κ4
end

function average_and_variance(ensemble_of_observable)
	ensemble_size = size(ensemble_of_observable, 2)
	average = reduce(+, eachcol(ensemble_of_observable)) ./ ensemble_size
	variance = reduce(+, eachcol((ensemble_of_observable .- average) .^ 2)) ./ (ensemble_size - 1)

	return average, variance
end

function bootstrap(df, attributes; num_resamples = 1000)
	@info "Computing observables using bootstrap method"
	nrows = nrow(df)

	original_sample = df[!, r"M_[1-99999]"]

	M_ensemble = Array{Float64, 2}(undef, nrows, num_resamples)
	M_abs_ensemble = Array{Float64, 2}(undef, nrows, num_resamples)
	χ_ensemble = Array{Float64, 2}(undef, nrows, num_resamples)
	κ3_ensemble = Array{Float64, 2}(undef, nrows, num_resamples)
	κ4_ensemble = Array{Float64, 2}(undef, nrows, num_resamples)

	Threads.@threads for i in ProgressBar(1:num_resamples, unit = "resamples", printing_delay = 1)
		M, M_abs, χ, κ3, κ4 = bootstrap_observables(original_sample, attributes)
		M_ensemble[:, i] = M
		M_abs_ensemble[:, i] = M_abs
		χ_ensemble[:, i] = χ
		κ3_ensemble[:, i] = κ3
		κ4_ensemble[:, i] = κ4
	end

	result = DataFrame()
	result[!, :t] = df[!, :t]
	result[!, :J] = df[!, :J]
	result[!, :M_avg], result[!, :M_var] = average_and_variance(M_ensemble)
	result[!, :M_abs_avg], result[!, :M_abs_var] = average_and_variance(M_abs_ensemble)
	result[!, :χ_avg], result[!, :χ_var] = average_and_variance(χ_ensemble)
	result[!, :κ3_avg], result[!, :κ3_var] = average_and_variance(κ3_ensemble)
	result[!, :κ4_avg], result[!, :κ4_var] = average_and_variance(κ4_ensemble)

	return result
end

function save_to_file(result, file_attr)
	D = file_attr["D"]
	N = file_attr["N"]
	T = file_attr["T"]
	q = file_attr["t_delta"]
	J_delta = file_attr["J_delta"]

	@info "Saving results to $(output_path)"
	if !isdir(output_path)
		mkpath(output_path)
	end

	if D == 2
		Tc = 4.4629
	elseif D == 3
		Tc = 9.37074
	else
		@error "Dimension needs to be 2 or 3."
	end

	τ = round((T - Tc) / Tc, digits = 6)
	ΔJ = round(file_attr["J_delta"], digits = 6)
	Δt = Int(file_attr["t_delta"])

	output_file = "$(D)D_N$(N)_τ$(τ)_dt$(Δt)_dJ$(ΔJ).h5"

	h5open(joinpath(output_path, output_file), "w") do file
		data = create_group(file, "data") # create a group
		data["t"] = result.t
		data["J"] = result.J
		data["M_avg"] = result.M_avg
		data["M_var"] = result.M_var
		data["M_abs_avg"] = result.M_abs_avg
		data["M_abs_var"] = result.M_abs_var
		data["χ_avg"] = result.χ_avg
		data["χ_var"] = result.χ_var
		data["κ3_avg"] = result.κ3_avg
		data["κ3_var"] = result.κ3_var
		data["κ4_avg"] = result.κ4_avg
		data["κ4_var"] = result.κ4_var

		HDF5.attributes(data)["D"] = D
		HDF5.attributes(data)["N"] = N
		HDF5.attributes(data)["T"] = T
		HDF5.attributes(data)["J_delta"] = J_delta
		HDF5.attributes(data)["t_delta"] = q
		HDF5.attributes(data)["mSq"] = file_attr["mSq"]
		HDF5.attributes(data)["lambda"] = file_attr["lambda"]
		HDF5.attributes(data)["gamma"] = file_attr["gamma"]
		HDF5.attributes(data)["n"] = file_attr["n"]
	end

	return nothing
end

function main()
	paths = rdir(base_path, "*.h5") # Recursively search for all .h5 files in the base path. And return a nested list of file paths.

	for files in paths
		path = replace(files[1], r"/[^/]+$" => "/") #Path to the folder containing multiple runs (.h5 files) with the same parameters.
		@assert isdir(path) "The specified path $path does not exist or is not a directory."
		@info "Reading files from path: $path"

		original_data, attributes = readfiles(files)
		bootstrap_result = bootstrap(original_data, attributes, num_resamples = 1000)
		save_to_file(bootstrap_result, attributes)
	end

	return true
end

# Run the main function if this file is executed directly
@static if (abspath(PROGRAM_FILE) == @__FILE__)
	main()
end


end # module Analysis