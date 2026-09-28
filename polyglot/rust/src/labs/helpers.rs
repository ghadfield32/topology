use std::fs;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone)]
pub struct LabResult {
    pub lab: String,
    pub title: String,
    pub metrics: Vec<(String, String)>,
    pub notes: Vec<String>,
}
impl LabResult {
    pub fn print_jsonish(&self) {
        println!("{{");
        println!("  \"lab\": {:?},", self.lab);
        println!("  \"title\": {:?},", self.title);
        println!("  \"metrics\": {{");
        for (i,(k,v)) in self.metrics.iter().enumerate() {
            let comma = if i + 1 == self.metrics.len() { "" } else { "," };
            println!("    {:?}: {}{}", k, v, comma);
        }
        println!("  }},");
        println!("  \"notes\": {:?}", self.notes);
        println!("}}");
    }
}
pub fn metric_num(name:&str,v:f64)->(String,String){(name.to_string(),format!("{v:.12}"))}
pub fn metric_int(name:&str,v:usize)->(String,String){(name.to_string(),v.to_string())}
pub fn metric_bool(name:&str,v:bool)->(String,String){(name.to_string(),v.to_string())}
pub fn metric_vec(name:&str,v:&[f64])->(String,String){(name.to_string(),format!("{:?}",v))}
pub fn l2(a:&[f64], b:&[f64])->f64 { a.iter().zip(b).map(|(x,y)|(x-y)*(x-y)).sum::<f64>().sqrt() }
pub fn dot(a:&[f64], b:&[f64])->f64 { a.iter().zip(b).map(|(x,y)|x*y).sum() }
pub fn rank_mod2(input:&[Vec<u8>])->usize { if input.is_empty(){return 0}; let mut a=input.to_vec(); let rows=a.len(); let cols=a[0].len(); let mut r=0usize; for c in 0..cols { if r>=rows{break}; let pivot=(r..rows).find(|&i|a[i][c]&1==1); let Some(p)=pivot else{continue}; a.swap(r,p); for i in 0..rows { if i!=r && a[i][c]&1==1 { for j in c..cols { a[i][j]^=a[r][j]; a[i][j]&=1; } } } r+=1; } r }
pub fn rotate_z(p:[f64;3],theta:f64)->[f64;3]{let(c,s)=(theta.cos(),theta.sin());[c*p[0]-s*p[1],s*p[0]+c*p[1],p[2]]}
pub fn weighted_mean(chunks:&[Vec<Vec<f64>>])->Vec<f64>{let d=chunks.iter().find_map(|c|c.first()).map(|p|p.len()).unwrap_or(0);let mut sum=vec![0.0;d];let mut n=0usize;for ch in chunks{for p in ch{for j in 0..d{sum[j]+=p[j];}n+=1;}}if n>0{for x in &mut sum{*x/=n as f64;}}sum}
pub fn equal_mean_chunk_means(chunks:&[Vec<Vec<f64>>])->Vec<f64>{if chunks.is_empty(){return vec![]};let d=chunks[0][0].len();let mut out=vec![0.0;d];for ch in chunks{let m=weighted_mean(&[ch.clone()]);for j in 0..d{out[j]+=m[j];}}for x in &mut out{*x/=chunks.len() as f64;}out}
pub fn repo_path(repo:&Path, rel:&str)->PathBuf{repo.join(rel.replace('/',std::path::MAIN_SEPARATOR_STR))}
pub fn csv_shape(path:&Path)->Result<(usize,usize),String>{let s=fs::read_to_string(path).map_err(|e|e.to_string())?;let mut lines=s.lines();let header=lines.next().ok_or("empty csv")?;let cols=header.split(',').count();let rows=lines.filter(|l|!l.trim().is_empty()).count();Ok((rows,cols))}
pub fn load_spl_ball(repo:&Path)->Result<Vec<Vec<f64>>,String>{let s=fs::read_to_string(repo_path(repo,"sports_v8/data/spl_selected_frames.json")).map_err(|e|e.to_string())?;let mut pts=Vec::new();let mut rest=s.as_str();while let Some(i)=rest.find("\"ball\""){rest=&rest[i+6..];let Some(lb)=rest.find('[') else{break};let Some(rb)=rest[lb+1..].find(']') else{break};let body=&rest[lb+1..lb+1+rb];let vals:Vec<f64>=body.split(',').filter_map(|x|x.trim().parse::<f64>().ok()).collect();if vals.len()==3{pts.push(vals.into_iter().map(|x|x*0.3048).collect());}rest=&rest[lb+1+rb+1..];}if pts.is_empty(){Err("no ball points parsed".into())}else{Ok(pts)}}
pub fn generic_stage(id:&str,title:&str)->Result<LabResult,String>{Ok(LabResult{lab:id.into(),title:title.into(),metrics:vec![metric_bool("implemented",true)],notes:vec!["Dependency-light companion; use the Python reference for the complete notebook workflow.".into()]})}
pub fn generic_case(repo:&Path,id:&str,title:&str,rel:&str)->Result<LabResult,String>{let(rows,cols)=csv_shape(&repo_path(repo,rel))?;Ok(LabResult{lab:id.into(),title:title.into(),metrics:vec![metric_int("data_rows",rows),metric_int("columns",cols)],notes:vec!["Schema/count companion; use the Python reference for the complete statistical protocol.".into()]})}
