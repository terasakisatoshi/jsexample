# ---
# jupyter:
#   jupytext:
#     formats: ipynb,jl:light
#     text_representation:
#       extension: .jl
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Julia 1.5.2
#     language: julia
#     name: julia-1.5
# ---

# # WebIO.jl Example

using WebIO
using JSExpr

# +
scope = Scope()
obs = Observable(scope, "rand-value", 0.0)

on(obs) do x
    println("JavaScript sent $(x)!")
end

scope(
    dom"button"(
        "Generate Random Number",
        events=Dict(
            "click" => @js () -> $obs[] = Math.random() + $obs[]
        ),
    ),
)

# -

# # Reference
#
# https://juliagizmos.github.io/WebIO.jl/latest/gettingstarted/#Sending-values-from-JavaScript-to-Julia
