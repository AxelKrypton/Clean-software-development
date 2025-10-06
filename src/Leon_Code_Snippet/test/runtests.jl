using Powerweek
using Test

@testset "All tests" begin
	@testset "Calling src/Powerweek.jl with mock data" begin
		@test begin
			test_success = true
			try
				run(`julia ../src/Powerweek.jl -i "../data" -o "./tmp"`)
			catch
				test_success = false
			end
			test_success
		end
		@test begin
			test_success = !isempty(readdir("./tmp"))
			if test_success
				# Clean up mock output files produced during testing
				rm("./tmp", recursive = true)
			end
			test_success
		end
	end

	@testset "Running some more tests..." begin
		@test 1 != 2
	end
end


