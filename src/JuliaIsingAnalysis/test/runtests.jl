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
        mock_wrongmin = [-1; -0.990; 1.0; -1.05; 0.5]
        mock_wrongmax = [-1; -0.990; 1.1; 1.0; 0.5]
        @test !checkDensities(Eggwin_df.e,-1,1)
        @test !checkDensities(Beaktrix_df.e,-1,1)
        @test !checkDensities(Siegfried_df.e,-1,1)
        @test !checkDensities(combined_df.e,-1,1)
        @test checkDensities(mock_wrongmin,-1,1)
        @test checkDensities(mock_wrongmax,-1,1)
    end

    @testset "magnetisation density should be between 0 and 1" begin
        mock_wrongmin = [-0.3; 0.990; 1.0; 0.34; 0.5]
        mock_wrongmax = [0; 0.990; 1.0; 0.34; 1.1]
        @test !checkDensities(Eggwin_df.abs_m,0,1)
        @test !checkDensities(Beaktrix_df.abs_m,0,1)
        @test !checkDensities(Siegfried_df.abs_m,0,1)
        @test !checkDensities(combined_df.abs_m,0,1)
        @test checkDensities(mock_wrongmin,0,1)
        @test checkDensities(mock_wrongmax,0,1)
    end

end