fn main() {
    let mut x = 5;

    let a = &mut x;
    *a += 1; // Last use of `a`: its borrow ends here.

    let b = &mut x;
    *b += 1;

    assert_eq!(x, 7);
}
