use minifb::{Key, Window, WindowOptions};

const W: usize = 400;
const H: usize = 240;

fn main(){
let mut fb=vec![0u32;W*H];
let mut w=Window::new("Neopunk Tunnel",W,H,WindowOptions::default()).unwrap();
let mut t=0.0f32;
while w.is_open()&&!w.is_key_down(Key::Escape){
for y in 0..H{
for x in 0..W{
let nx=x as f32/W as f32-0.5;
let ny=y as f32/H as f32-0.5;
let r=(nx*nx+ny*ny).sqrt();
let a=ny.atan2(nx);
let z=(r*10.0-t).sin();
let c=((a*3.0+z)*128.0+128.0)as u32;
fb[y*W+x]=(c<<16)|(c<<8)|c;
}
}
w.update_with_buffer(&fb,W,H).unwrap();
t+=0.05;
}
}