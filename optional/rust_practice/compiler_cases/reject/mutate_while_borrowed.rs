fn main() {
    let mut points = vec![[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]];

    let first = &points[0];
    points[1][0] = 5.0;

    println!("{}", first[0]);
}
