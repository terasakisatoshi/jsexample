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
#     display_name: Julia 1.5.3
#     language: julia
#     name: julia-1.5
# ---

using Genie; up()

# +
route("/hello") do; "Welcome to Genie!" ;end

HTML("""
<iframe src="http://localhost:8000/hello" width="800" height="100"></iframe>
""")
