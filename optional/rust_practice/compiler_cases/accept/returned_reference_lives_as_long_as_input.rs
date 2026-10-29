fn label<'a>(text: &'a str) -> &'a str {
    text
}

fn main() {
    let owned = String::from("observed");
    let borrowed = label(&owned);
    assert_eq!(borrowed, "observed");
}
