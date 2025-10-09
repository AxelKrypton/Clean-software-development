module JuliaIsingAnalysis

using DelimitedFiles, DataFrames

path = "../../Ising2D/Eggwin/Ising_2D_MCMC_Ns8_Ns8/temp0.5.txt"


function readEggwinFile(path::String)

	data, header = readdlm(path, header = true);
	df = DataFrame(data[:, 1:3], ["Configuration", "E", "M"])

	V = 8*8
	T = split(split(path, "temp")[2], ".txt")[1]

	df["T"] = T
	df["V"] = V
end

function readBeaktrixFile(path::String)
end


end # module JuliaIsingAnalysis
