use std::{env,path::PathBuf,process};
fn main(){
    let mut repo=PathBuf::from("../.."); let mut lab=String::from("stage01"); let mut list=false;
    let mut args=env::args().skip(1);
    while let Some(a)=args.next(){match a.as_str(){"--repo"=>{repo=PathBuf::from(args.next().unwrap_or_default())},"--lab"=>{lab=args.next().unwrap_or_default()},"--list"=>list=true,_=>{eprintln!("unknown arg {a}");process::exit(2)}}}
    if list {let mut ids=listening_to_shape_rust::labs::ids();ids.sort();for id in ids{println!("{id}");}return;}
    match listening_to_shape_rust::labs::run(&repo,&lab){Ok(r)=>r.print_jsonish(),Err(e)=>{eprintln!("{e}");process::exit(1)}}
}
