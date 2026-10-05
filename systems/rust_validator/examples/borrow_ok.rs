fn main(){let mut x=5;{let a=&mut x;*a+=1;}let b=&mut x;*b+=1;assert_eq!(x,7);println!("{x}");}
