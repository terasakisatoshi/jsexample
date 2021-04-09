let dom = document.querySelector("#root");
let element = React.createElement(
    "div", {},[
        React.createElement(
            "h2", {}, "Hi",
        ),
        React.createElement(
            "h3", {className:"alert alert-primary"}, "React sample page",
        ),
        React.createElement(
            "ul", {className:"list-group"}, [
                React.createElement(
                    "li", {className:"list-group-item"}, "item1"
                ),
                React.createElement(
                    "li", {className:"list-group-item"}, "item2"
                ),
                React.createElement(
                    "li", {className:"list-group-item"}, "item3"
                ),
            ]
        )
    ]
)

ReactDOM.render(element, dom);