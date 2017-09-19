// === Vector ===
function Vec3(x, y, z) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.length = this._length();
}

Vec3.__test__ = function() {
    var a = new Vec3(1, 0, 0);
    var b = new Vec3(0, 1, 0);
    var c = new Vec3(1, 2, 2);

    console.assert(a.cross(b).equals(new Vec3(0, 0, 1)));
    console.assert(a.dot(b) == 0);
    console.assert(c.length == 3);
}

Vec3.prototype.equals = function(other) {
    // compare this to other
    return this.x == other.x && this.y == other.y && this.z == other.z;
}


Vec3.prototype._length = function() {
    return Math.sqrt(this.x**2 + this.y**2 + this.z**2);
}

Vec3.prototype.multiply = function (scalar) {
    // return product of this and a scalar
    return new Vec3(this.x*scalar, this.y*scalar, this.z*scalar);
}

Vec3.prototype.divide = function (scalar) {
    // return quotient of this and a scalar
    return new Vec3(this.x/scalar, this.y/scalar, this.z/scalar);
}

Vec3.prototype.add = function (other) {
    // adds to other
    var x,y,z;
    x = this.x + other.x;
    y = this.y + other.y;
    z = this.z + other.z;
    return new Vec3(x,y,z);
}

Vec3.prototype.subtract = function (other) {
    // subtract other from this
    return this.add(other.multiply(-1));
}

Vec3.prototype.unitvector = function() {
    // return the unit vector with this vector's direction.
    return this.multiply(1 / this.length);
}

Vec3.prototype.cross = function (other) {
    // return the cross product of this and other
    var x,y,z;
    x = this.y*other.z - this.z*other.y;
    y = this.z*other.x - this.x*other.z;
    z = this.x*other.y - this.y*other.x;
    return new Vec3(x,y,z);
}

Vec3.prototype.dot = function(other) { 
    // return the dot product of this and other
    return this.x*other.x + this.y*other.y + this.z*other.z;
}

// === Plane ===
function Plane(p0, n) {
    this.p0 = p0;           // a point in the plane
    this.n = n.unitvector;  // a vector normal to the plane
}

// === Line ===
function Line(p0, d) {
    this.p0 = p0;              // a point on the line
    this.d = d.unitvector;     // the direction of the line
}
