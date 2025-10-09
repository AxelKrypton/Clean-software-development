using Test

include("../src/JuliaIsingAnalysis.jl")

function checkDensities(clmn,min,max)
    flag = false
    for element in clmn 
        if element < min || element > max
            flag = true 
            break
        end 
    end 
    return flag
end




@testset "All tests" begin 

    @testset "Energy density should be between -1 and 1" begin
        @test !checkDensities(Eggwin_df.e,-1,1)
    end

    


end