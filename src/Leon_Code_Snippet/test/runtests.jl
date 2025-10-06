using Test
using Random, Statistics
using DataFrames
using Distributions
using HDF5
using Unicode

# --- import your module ---
include(joinpath(@__DIR__, "..", "src", "Powerweek.jl"))
using .Powerweek

# -------------------------------
# helpers to make mock data/files
# -------------------------------
function mock_attributes(; D=2, N=4, T=1.0, JΔ=1.0, tΔ=10.0, mSq=1.0, λ=1.0, γ=1.0, n=9, precision=64)
    return Dict(
        "J_delta" => JΔ,
        "t_delta" => tΔ,
        "T" => T,
        "N" => N,
        "mSq" => mSq,
        "gamma" => γ,
        "D" => D,
        "lambda" => λ,
        "n" => n,
        "precision" => precision,
    )
end

"Create DF with columns: t, J, and M_1..M_k containing lognormal mock data."
function mock_df(nrows::Int, k::Int; rng=MersenneTwister(123), μ=0.0, σ=0.6)
    df = DataFrame()
    df.t = collect(1:nrows)
    df.J = fill(0.0, nrows)
    d = LogNormal(μ, σ)
    for j in 1:k
        df[!, Symbol("M_$(j)")] = rand(rng, d, nrows)
    end
    return df
end

"Write a minimal HDF5 file matching Powerweek.readfiles expectations."
function write_mock_h5(path::AbstractString; t::AbstractVector, J::AbstractVector, M::AbstractVector, attrs::Dict)
    mkpath(dirname(path))
    h5open(path, "w") do f
        g = create_group(f, "data")
        g["t"] = t
        g["J"] = J
        g["M"] = M
        HDF5.attributes(g)["T"] = attrs["T"]
        HDF5.attributes(g)["N"] = attrs["N"]
        HDF5.attributes(g)["mSq"] = attrs["mSq"]
        HDF5.attributes(g)["gamma"] = attrs["gamma"]
        HDF5.attributes(g)["D"] = attrs["D"]
        HDF5.attributes(g)["lambda"] = attrs["lambda"]
        HDF5.attributes(g)["precision"] = attrs["precision"]
    end
    return path
end

# tiny helper for attribute values
attv(g, key) = read(HDF5.attributes(g)[key])

# ===========================================================
# Tests
# ===========================================================

@testset "average_and_variance" begin
    # 3 rows, 4 columns (resamples)
    A = [1.0 2 3 4;
         2.0 2 2 2;
         5.0 5 5 7]
    avg, var = Powerweek.average_and_variance(A)

    @test avg ≈ [2.5, 2.0, 5.5]
    # sample variance across columns (n-1 denominator)
    @test var  ≈ [1.6666666667, 0.0, 1.0] atol=1e-10
end

@testset "bootstrap_observables basics + V/T scaling" begin
    df = mock_df(500, 9)                        # M_1..M_9
    original_single_digit = df[!, r"^M_\d$"]    # pass directly

    attrs = mock_attributes(D=2, N=4, T=2.0)    # V/T = 16/2 = 8
    Random.seed!(2024)
    M, Mabs, χ, κ3, κ4 = Powerweek.bootstrap_observables(original_single_digit, attrs)

    # length check (map length over tuple)
    @test all(==(500), map(length, (M, Mabs, χ, κ3, κ4)))
    @test all(isfinite, M)
    @test all(x -> x ≥ 0, Mabs)
    @test all(isfinite, χ)
    @test all(isfinite, κ3)
    @test all(isfinite, κ4)

    # deterministic V/T scaling: reseed so same resample is used
    attrs2 = mock_attributes(D=2, N=8, T=1.0)   # V/T = 64/1 = 64
    Random.seed!(2024)
    _, _, χ1, _, _ = Powerweek.bootstrap_observables(original_single_digit, attrs)
    Random.seed!(2024)
    _, _, χ2, _, _ = Powerweek.bootstrap_observables(original_single_digit, attrs2)

    s1 = (attrs["N"]^attrs["D"]) / attrs["T"]
    s2 = (attrs2["N"]^attrs2["D"]) / attrs2["T"]
    scale = s2 / s1  # 8.0

    @test χ2 ≈ scale .* χ1 atol=1e-9
end

@testset "bootstrap end-to-end (DF input)" begin
    attrs = mock_attributes(D=3, N=4, T=1.2)
    df = mock_df(300, 9)  # M_1..M_9

    res = Powerweek.bootstrap(df, attrs; num_resamples=50)

    # Use normalized strings for robust Unicode symbol comparison
    need_str = [
        "t","J","M_avg","M_var","M_abs_avg","M_abs_var",
        "χ_avg","χ_var","κ3_avg","κ3_var","κ4_avg","κ4_var",
    ]
    have_str = Unicode.normalize.(String.(names(res)))
    missing = setdiff(Set(need_str), Set(have_str))
    @test isempty(missing)
    @test nrow(res) == 300
    @test all(x -> all(>(-1e-12), x), (res.M_var, res.M_abs_var, res.χ_var, res.κ3_var, res.κ4_var))
end


@testset "save_to_file writes expected dataset + attrs (temp cwd)" begin
    mktempdir() do tmp
        cd(tmp) do
            attrs = mock_attributes(D=2, N=8, T=1.5, JΔ=0.25, tΔ=20.0, n=9)
            df = mock_df(120, 9)
            res = Powerweek.bootstrap(df, attrs; num_resamples=20)

            # compute expected filename
            D = attrs["D"]; N = attrs["N"]; T = attrs["T"]; q = attrs["t_delta"]; ΔJ = attrs["J_delta"]
            Tc = D == 2 ? 4.4629 : 9.37074
            τ = round((T - Tc) / Tc, digits = 6)
            Δt = Int(q)
            outfile = "$(D)D_N$(N)_τ$(τ)_dt$(Δt)_dJ$(round(ΔJ, digits=6)).h5"

            # try 2-arg; if it errors, call 3-arg with an explicit outdir
            wrote_dir = nothing
            try
                Powerweek.save_to_file(res, attrs)
                wrote_dir = joinpath("data", "averaged")
            catch e
                if e isa MethodError
                    outdir = mkpath(joinpath(tmp, "data", "averaged"))
                    Powerweek.save_to_file(res, attrs, outdir)  # 3-arg form
                    wrote_dir = outdir
                else
                    rethrow()
                end
            end

            fullpath = joinpath(wrote_dir, outfile)
            @test isfile(fullpath)

            h5open(fullpath, "r") do f
                @test haskey(f, "data")
                g = f["data"]
                @test length(read(g["t"])) == 120
                @test length(read(g["J"])) == 120
                for name in ["M_avg","M_var","M_abs_avg","M_abs_var","χ_avg","χ_var","κ3_avg","κ3_var","κ4_avg","κ4_var"]
                    @test haskey(g, name)
                    @test length(read(g[name])) == 120
                end
                # attrs helper
                attv(g, key) = read(HDF5.attributes(g)[key])
                @test attv(g, "D")       == attrs["D"]
                @test attv(g, "N")       == attrs["N"]
                @test attv(g, "T")       == attrs["T"]
                @test attv(g, "J_delta") == attrs["J_delta"]
                @test attv(g, "t_delta") == attrs["t_delta"]
                @test attv(g, "n")       == attrs["n"]
            end
        end
    end
end
@testset "readfiles + bootstrap from real HDF5 inputs (end-to-end)" begin
    mktempdir() do tmp
        data_dir = joinpath(tmp, "inputs")
        nfiles = 5
        nrows = 50
        t = collect(range(-2.0, 2.0, length=nrows))
        J = zeros(nrows)
        attrs = mock_attributes(D=2, N=6, T=2.0, precision=64, n=nfiles)

        rng = MersenneTwister(42)
        σ = 0.7
        for i in 1:nfiles
            μ = 0.1 * (i-1)
            M = rand(rng, LogNormal(μ, σ), nrows)
            write_mock_h5(joinpath(data_dir, "run_$(i).h5"); t=t, J=J, M=M, attrs=attrs)
        end

        files = filter(endswith(".h5"), sort(readdir(data_dir; join=true)))
        df, attrs_out = Powerweek.readfiles(files)

        @test nrow(df) == nrows
        @test haskey(attrs_out, "T") && attrs_out["T"] == attrs["T"]

        
        have = names(df)                              # Vector{String}

        @test "t" in have && "J" in have              # must have t and J

        ms = filter(n -> startswith(n, "M_"), have)   # all M_* columns
        idx = sort(parse.(Int, last.(split.(ms, "_"))))  # [1,2,3,...,k]

        @test idx == collect(1:length(idx))           # contiguous M_1..M_k
        res = Powerweek.bootstrap(df, attrs_out; num_resamples=60)
        @test nrow(res) == nrows
        @test all(x -> all(isfinite, x), (res.M_avg, res.M_abs_avg, res.χ_avg, res.κ3_avg, res.κ4_avg))
    end
end
