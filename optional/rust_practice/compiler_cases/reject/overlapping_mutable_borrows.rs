fn main() {
    let mut x = 5;

    let a = &mut x;
    let b = &mut x;

    println!("{a} {b}");
}
