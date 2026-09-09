import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import "./index.css";

const API = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, "");

type User = { id:number; email:string; full_name?:string|null; bio?:string|null; profile_picture?:string|null; created_at:string };
type Media = { id:number; file_url:string; file_type:string; mime_type:string; file_size:number };
type Post = { id:number; title:string; content:string; published:boolean; created_at:string; owner_id:number; owner:User; media:Media[] };
type PostOut = { Post:Post; vote:number };
type Story = { id:number; owner_id:number; file_url:string; file_type:string; mime_type:string; file_size:number; expires_at:string; created_at:string };
type Message = { id:number; sender_id:number; receiver_id:number; message:string; is_read:boolean; created_at:string };

const client = axios.create({ baseURL: API });
client.interceptors.request.use(c => {
  const token = localStorage.getItem("token");
  if (token) c.headers.Authorization = `Bearer ${token}`;
  return c;
});

function mediaUrl(path?:string|null) {
  if (!path) return "";
  if (/^https?:\/\//.test(path)) return path;
  return `${API}/${path.replace(/^\/+/, "")}`;
}

export default function App() {
  const [token,setToken]=useState(localStorage.getItem("token"));
  const [page,setPage]=useState("home");
  const [me,setMe]=useState<User|null>(null);

  const logout=()=>{ localStorage.removeItem("token"); setToken(null); setMe(null); setPage("home"); };

  useEffect(()=>{ if(token) client.get<User>("/auth/me").then(r=>setMe(r.data)).catch(()=>logout()); },[token]);

  if(!token) return <Auth onLogin={t=>{localStorage.setItem("token",t);setToken(t)}} />;

  return <div className="app">
    <header className="topbar">
      <button className="brand" onClick={()=>setPage("home")}>CRUD</button>
      <nav>
        <button onClick={()=>setPage("home")}>Posts</button>
        <button onClick={()=>setPage("stories")}>Stories</button>
        <button onClick={()=>setPage("messages")}>Messages</button>
        <button onClick={()=>setPage("profile")}>Profile</button>
        <button onClick={logout}>Logout</button>
      </nav>
    </header>
    <main>
      {page==="home" && <Home me={me} goProfile={()=>setPage("profile")} />}
      {page==="profile" && me && <Profile me={me} />}
      {page==="stories" && <Stories />}
      {page==="messages" && me && <Messages me={me} />}
    </main>
  </div>
}

function Auth({onLogin}:{onLogin:(t:string)=>void}) {
  const [register,setRegister]=useState(false);
  const [email,setEmail]=useState(""); const [password,setPassword]=useState(""); const [name,setName]=useState(""); const [bio,setBio]=useState("");
  const [error,setError]=useState("");
  async function submit(e:React.FormEvent){
    e.preventDefault(); setError("");
    try {
      if(register){
        const r=await client.post("/auth/register",{email,password,full_name:name||null,bio:bio||null});
        onLogin(r.data.access_token);
      } else {
        const body=new URLSearchParams({username:email,password});
        const r=await client.post("/auth/login", body, { headers: { "Content-Type": "application/x-www-form-urlencoded" } });
        onLogin(r.data.access_token);
      }
    } catch(err:any){ setError(err.response?.data?.detail || "Request failed"); }
  }
  return <div className="auth"><form className="card" onSubmit={submit}>
    <h1>CRUD</h1><p className="muted">{register?"Create an account":"Sign in"}</p>
    {register && <><label>Full name<input value={name} onChange={e=>setName(e.target.value)} /></label><label>Bio<textarea value={bio} onChange={e=>setBio(e.target.value)} /></label></>}
    <label>Email<input type="email" required value={email} onChange={e=>setEmail(e.target.value)} /></label>
    <label>Password<input type="password" required value={password} onChange={e=>setPassword(e.target.value)} /></label>
    {error&&<div className="error">{error}</div>}<button className="primary">{register?"Register":"Login"}</button>
    <button type="button" className="link" onClick={()=>setRegister(!register)}>{register?"Already have an account? Login":"Create an account"}</button>
  </form></div>
}

function Home({me}:{me:User|null;goProfile:()=>void}) {
  const [posts,setPosts]=useState<PostOut[]>([]); const [loading,setLoading]=useState(true); const [error,setError]=useState("");
  const [showCreate,setShowCreate]=useState(false);
  async function load(){try{setLoading(true); const r=await client.get<PostOut[]>("/posts/?limit=100&skip=0");setPosts(r.data)}catch(e:any){setError(e.response?.data?.detail||"Could not load posts")}finally{setLoading(false)}}
  useEffect(()=>{load()},[]);
  return <section>
    <div className="page-head"><div><h2>Posts</h2><p className="muted">Simple CRUD feed</p></div><button className="primary" onClick={()=>setShowCreate(true)}>Create post</button></div>
    {showCreate&&<CreatePost close={()=>setShowCreate(false)} done={load}/>}
    {error&&<div className="error">{error}</div>}
    {loading?<p>Loading...</p>:posts.length?<div className="feed">{posts.map(x=><PostCard key={x.Post.id} item={x} me={me} refresh={load}/>)}</div>:<div className="card empty">No posts yet.</div>}
  </section>
}

function CreatePost({close,done}:{close:()=>void;done:()=>void}) {
  const [title,setTitle]=useState(""); const [content,setContent]=useState(""); const [file,setFile]=useState<File|null>(null); const [error,setError]=useState(""); const [busy,setBusy]=useState(false);
  async function submit(e:React.FormEvent){e.preventDefault();setError("");setBusy(true);
    try{
      const r=await client.post<Post>("/posts/",{title:title||content.slice(0,60)||"Post",content,published:true});
      if(file){const fd=new FormData();fd.append("post_id",String(r.data.id));fd.append("file",file);await client.post("/media/upload",fd);}
      close();done();
    }catch(e:any){setError(e.response?.data?.detail||JSON.stringify(e.response?.data)||"Could not create post")}finally{setBusy(false)}
  }
  return <div className="card composer"><div className="page-head"><h3>New post</h3><button onClick={close}>Cancel</button></div>
    <form onSubmit={submit}><label>Title<input value={title} onChange={e=>setTitle(e.target.value)} /></label><label>Content<textarea required rows={6} value={content} onChange={e=>setContent(e.target.value)} /></label>
    <label>Photo or video<input type="file" accept="image/*,video/*" onChange={e=>setFile(e.target.files?.[0]||null)} /></label>
    {file&&<p className="muted">{file.name}</p>}{error&&<div className="error">{error}</div>}<button className="primary" disabled={busy}>{busy?"Posting...":"Post"}</button></form>
  </div>
}

function PostCard({item,me,refresh}:{item:PostOut;me:User|null;refresh:()=>void}) {
  const p=item.Post; const [busy,setBusy]=useState(false); const [saved,setSaved]=useState(false);
  async function vote(dir:number){try{setBusy(true);await client.post("/vote/",{post_id:p.id,dir});refresh()}catch(e:any){alert(e.response?.data?.detail||"Vote failed")}finally{setBusy(false)}}
  async function bookmark(){try{if(!saved){await client.post("/bookmarks/",{post_id:p.id});setSaved(true)}else{await client.delete(`/bookmarks/${p.id}`);setSaved(false)}}catch(e:any){alert(e.response?.data?.detail||"Save failed")}}
  async function remove(){if(!confirm("Delete this post?"))return;try{await client.delete(`/posts/${p.id}`);refresh()}catch(e:any){alert(e.response?.data?.detail||"Delete failed")}}
  return <article className="card post">
    <div className="post-author"><strong>{p.owner?.full_name||p.owner?.email||`User ${p.owner_id}`}</strong><span className="muted">{new Date(p.created_at).toLocaleString()}</span></div>
    <h3>{p.title}</h3><p>{p.content}</p>
    {p.media?.map(m=><div key={m.id} className="media">{m.file_type==="video"?<video controls src={mediaUrl(m.file_url)}/>:<img src={mediaUrl(m.file_url)} alt="" />}</div>)}
    <div className="actions"><button disabled={busy} onClick={()=>vote(1)}>♥ {item.vote}</button><button disabled={busy} onClick={()=>vote(0)}>Unlike</button><button onClick={bookmark}>{saved?"Saved":"Save"}</button>{me?.id===p.owner_id&&<button onClick={remove}>Delete</button>}</div>
  </article>
}

function Profile({me}:{me:User}) {
  const [posts,setPosts]=useState<PostOut[]>([]);const [full,setFull]=useState(me.full_name||"");const [bio,setBio]=useState(me.bio||"");const [file,setFile]=useState<File|null>(null);const [msg,setMsg]=useState("");
  async function load(){try{const r=await client.get<PostOut[]>("/posts/?limit=100&skip=0");setPosts(r.data.filter(x=>x.Post.owner_id===me.id))}catch{}}
  useEffect(()=>{load()},[me.id]);
  async function save(){try{await client.put(`/users/${me.id}`,{full_name:full,bio});setMsg("Profile updated")}catch(e:any){setMsg(e.response?.data?.detail||"Update failed")}}
  async function upload(){if(!file)return;try{const fd=new FormData();fd.append("file",file);await client.put(`/users/${me.id}/profile-picture`,fd);setMsg("Profile picture updated")}catch(e:any){setMsg(e.response?.data?.detail||"Upload failed")}}
  return <section><div className="card profile">
    <div className="profile-top">{me.profile_picture?<img className="avatar large" src={mediaUrl(me.profile_picture)} />:<div className="avatar large">{(me.full_name||me.email)[0].toUpperCase()}</div>}<div><h2>{me.full_name||"My profile"}</h2><p className="muted">{me.email}</p></div></div>
    <label>Full name<input value={full} onChange={e=>setFull(e.target.value)}/></label><label>Bio<textarea value={bio} onChange={e=>setBio(e.target.value)}/></label>
    <div className="row"><button className="primary" onClick={save}>Save profile</button><input type="file" accept="image/*" onChange={e=>setFile(e.target.files?.[0]||null)}/><button onClick={upload}>Upload picture</button></div>{msg&&<p className="muted">{msg}</p>}
  </div><h2>My posts</h2>{posts.length?<div className="feed">{posts.map(x=><PostCard key={x.Post.id} item={x} me={me} refresh={load}/>)}</div>:<div className="card empty">No posts yet.</div>}</section>
}

function Stories(){
 const [stories,setStories]=useState<Story[]>([]);const [file,setFile]=useState<File|null>(null);const [error,setError]=useState("");
 async function load(){try{const r=await client.get<Story[]>("/stories/");setStories(r.data)}catch(e:any){setError(e.response?.data?.detail||"Could not load stories")}}
 useEffect(()=>{load()},[]);
 async function upload(){if(!file)return;try{const fd=new FormData();fd.append("file",file);await client.post("/stories/",fd);setFile(null);load()}catch(e:any){setError(e.response?.data?.detail||"Upload failed")}}
 return <section><div className="page-head"><div><h2>Stories</h2><p className="muted">Stories expire after 24 hours.</p></div></div><div className="card"><input type="file" accept="image/*,video/*" onChange={e=>setFile(e.target.files?.[0]||null)}/><button className="primary" onClick={upload} disabled={!file}>Upload story</button>{error&&<div className="error">{error}</div>}</div><div className="story-grid">{stories.map(s=><div className="card" key={s.id}>{s.file_type==="video"?<video controls src={mediaUrl(s.file_url)}/>:<img src={mediaUrl(s.file_url)} alt="" />}<small>User {s.owner_id}</small></div>)}</div></section>
}

function Messages({me}:{me:User}){
 const [other,setOther]=useState("");const [messages,setMessages]=useState<Message[]>([]);const [text,setText]=useState("");const [error,setError]=useState("");
 async function load(){if(!other)return;try{const r=await client.get<Message[]>(`/messages/conversation/${Number(other)}`);setMessages(r.data)}catch(e:any){setError(e.response?.data?.detail||"Could not load conversation")}}
 async function send(){if(!other||!text.trim())return;try{const r=await client.post<Message>("/messages/",{receiver_id:Number(other),message:text});setMessages(x=>[...x,r.data]);setText("")}catch(e:any){setError(e.response?.data?.detail||"Send failed")}}
 return <section><h2>Messages</h2><div className="card"><label>Other user ID<input type="number" value={other} onChange={e=>setOther(e.target.value)}/></label><button onClick={load}>Load conversation</button>{error&&<div className="error">{error}</div>}<div className="messages">{messages.map(m=><div className={m.sender_id===me.id?"mine":"theirs"} key={m.id}><span>{m.message}</span><small>{new Date(m.created_at).toLocaleString()}</small></div>)}</div><div className="row"><input placeholder="Message" value={text} onChange={e=>setText(e.target.value)} onKeyDown={e=>e.key==="Enter"&&send()}/><button className="primary" onClick={send}>Send</button></div></div></section>
}
