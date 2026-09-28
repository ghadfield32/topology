use shape_native::{data, labs};
use std::{env, fs, panic, path::Path};
fn main() {
    let code = match panic::catch_unwind(run) {
        Ok(Ok(())) => 0,
        Ok(Err(e)) => {
            eprintln!("ERROR: {e}");
            1
        }
        Err(e) => {
            let msg = e
                .downcast_ref::<String>()
                .map(String::as_str)
                .or_else(|| e.downcast_ref::<&str>().copied())
                .unwrap_or("native computation failed");
            eprintln!("ERROR: {msg}");
            1
        }
    };
    std::process::exit(code);
}
fn run() -> Result<(), String> {
    let (mut repo, mut lab, mut decode, mut output) =
        (".".to_string(), String::new(), String::new(), String::new());
    let mut list = false;
    let args: Vec<String> = env::args().skip(1).collect();
    let mut i = 0;
    while i < args.len() {
        match args[i].as_str() {
            "--list" => list = true,
            "--repo" | "--lab" | "--decode" | "--output" => {
                let key = &args[i];
                i += 1;
                let v = args.get(i).ok_or("missing flag value")?.clone();
                match key.as_str() {
                    "--repo" => repo = v,
                    "--lab" => lab = v,
                    "--decode" => decode = v,
                    _ => output = v,
                }
            }
            "--help" | "-h" => {
                println!("shape-rust --repo COURSE_ROOT [--list | --lab KEY | --decode RELATIVE_PATH] [--output NEW_DIRECTORY]");
                return Ok(());
            }
            x => return Err(format!("unknown argument {x}")),
        }
        i += 1;
    }
    if !output.is_empty() && Path::new(&output).exists() {
        return Err("output exists; choose a new directory".into());
    }
    let result = if list {
        serde_json::json!(labs::lab_keys(&repo))
    } else if !decode.is_empty() {
        data::decode(&repo, &decode)
    } else {
        labs::run(&repo, &lab)
    };
    let bytes = serde_json::to_vec_pretty(&result).map_err(|e| e.to_string())?;
    if output.is_empty() {
        println!("{}", String::from_utf8(bytes).unwrap());
    } else {
        let p = Path::new(&output);
        if let Some(parent) = p.parent() {
            if !parent.as_os_str().is_empty() {
                fs::create_dir_all(parent).map_err(|e| e.to_string())?;
            }
        }
        fs::create_dir(p).map_err(|e| e.to_string())?;
        fs::write(p.join("result.json"), bytes).map_err(|e| e.to_string())?;
        println!("{}", p.join("result.json").display());
    }
    Ok(())
}
