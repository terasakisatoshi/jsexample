# -*- coding: utf-8 -*-
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

using WebIO
using JSExpr

# +
s = Scope(
      imports = [
        "./vars.js",
        "./mystyle.css",
    　],
)

b = Node(
    :button, 
    "press",
    className="button",
    events=Dict(
        "click" => js"""
        function () {
            const old = document.querySelector(".button")
                                 .textContent;
            if(old == "pressed"){
                document.querySelector(".button")
                        .textContent = "press";
            } else {
                document.querySelector(".button")
                        .textContent = "pressed";
            }
            console.log(myVar);
            console.log(f(3));
        }
        """
    )
)

d = Node(
    :div,
    "A",
    className="rectangle",
)

s(Node(:div, b, d))
# -


