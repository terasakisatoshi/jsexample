using JSXGraph

brd = board("brd",xlim=[-15,15], ylim=[-15,15],axis=true)

a = slider("a", [[8, 7], [12, 7], [-3, 0.1, 10]])
b = slider("b", [[8, 6], [12, 6], [-1, 1, 5]])
c = slider("c", [[8, 5], [12, 5], [-10, -5, 2]])
[a,b,c] |> brd

@jsf f(x) = val(a) * x^2 + val(b) * x + val(c)

brd ++ plot(f)
brd.style="width:500px;height:500px;margin:0 auto;"
