using Powerweek
using Test

@testset "Running some tests.." begin
	@test 1 == 1
	@test 1 < 2
end

@testset "Running some more tests.." begin
	@test 1 != 2
end


