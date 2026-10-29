fn local_label() -> &str {
    let owned = String::from("temporary");
    &owned
}

fn main() {
    println!("{}", local_label());
}
