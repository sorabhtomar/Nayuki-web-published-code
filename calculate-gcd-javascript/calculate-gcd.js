/* 
 * GCD calculator
 * 
 * Copyright (c) 2014 Project Nayuki
 * All rights reserved. Contact Nayuki for licensing.
 * https://www.nayuki.io/page/calculate-gcd-javascript
 */

"use strict";


/* 
 * Handles the HTML input/output for calculating the GCD of two integers.
 * This is the one and only entry point function called from the HTML code.
 */
function calculate() {
	var xStr = document.getElementById("numberX").value;
	var yStr = document.getElementById("numberY").value;
	var output;
	if (xStr == "" || yStr == "")
		output = "";
	else if (!isInteger(xStr) || !isInteger(yStr))
		output = "Not an integer";
	else {
		var x = parseInt(xStr, 10);
		var y = parseInt(yStr, 10);
		if (x < 0 || x >= 9007199254740992 || y < 0 || y >= 9007199254740992)
			output = "Number out of range";
		else
			output = gcd(Math.abs(x), Math.abs(y)).toString(10);
	}
	document.getElementById("output").value = output;
}


// Returns the GCD of the given integers. Each input must be non-negative.
function gcd(x, y) {
	while (y != 0) {
		var z = x % y;
		x = y;
		y = z;
	}
	return x;
}


// Tests whether the given string represents an integer.
function isInteger(str) {
	return /^-?\d+$/.test(str);
}
