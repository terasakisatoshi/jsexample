// ---
// jupyter:
//   jupytext:
//     formats: ipynb,js:light
//     text_representation:
//       extension: .js
//       format_name: light
//       format_version: '1.5'
//       jupytext_version: 1.6.0
//   kernelspec:
//     display_name: Javascript (Node.js)
//     language: javascript
//     name: javascript
// ---

// # How to install kernel for NodeJS

// Install Python(for jupyter) and NodeJS(for npm)
//
// ```console
// npm install -g ijavascript
// ijsinstall
// ```

// # References
//
// https://developer.mozilla.org/ja/

// # Say Hello

console.log("Hello")

// # Easy Math

console.log(1+1)
console.log(1-1)
console.log(2*3)
console.log(2/3)
console.log(7%2)
console.log(2**3)

// # String interpolation
//
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals
//

var myName = "goma"
console.log(`My Name is ${myName}`)

// # Array

// +
var catNamesArray = ["Jacqueline", "Sophia", "Autumn"];

console.log(catNamesArray[0])
console.log(catNamesArray[1])
console.log(catNamesArray[2])
// -

// ## Slice

// +
var myArray = [-1,-2,-3,-4,-5,-6]

console.log(myArray.slice(2, 5))
// -

// # Functions

// +
function sayHello(msg){
    console.log(`Hello ${msg}`)
}

sayHello("World")

const sumTriplet = (a,b,c) => a+b+c;

sumTriplet(1,2,3)

// +
function sumAll(...numbers){
    let s = 0;
    for(const v of numbers) {
        s += v;
    }
    return s;
}

console.log(sumAll(1,2,3))
console.log(sumAll(1,2,3,4,5,6,7,8,9,10))
