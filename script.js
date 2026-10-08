const ADMIN_EMAIL="admin@campus.360";
const ADMIN_PASSWORD="Campus360@Admin2026";

document.getElementById("loginForm").addEventListener("submit",function(e){
  e.preventDefault();
  const email=document.getElementById("email").value.trim().toLowerCase();
  const password=document.getElementById("password").value;

  if(!email.endsWith("@campus.360")){
    alert("Use your official @campus.360 account.");
    return;
  }
  if(email===ADMIN_EMAIL && password===ADMIN_PASSWORD){
    document.querySelector(".hero").hidden=true;
    document.getElementById("dashboard").hidden=false;
    window.scrollTo({top:0,behavior:"smooth"});
    return;
  }
  alert("Invalid credentials. Student accounts must be created by the administrator.");
});

function logout(){
  document.querySelector(".hero").hidden=false;
  document.getElementById("dashboard").hidden=true;
  document.getElementById("password").value="";
}

function sos(){
  const ok=confirm("Emergency SOS: call campus emergency support?");
  if(ok) window.location.href="tel:112";
}

function openComplaint(){
  alert("Complaint module: connect this button to your Flask backend/API when deploying the full application.");
}
function showStatus(){
  alert("Complaint tracking module: connect this button to your Flask backend/API.");
}
function showHelp(){
  document.getElementById("chat").scrollIntoView({behavior:"smooth"});
  document.getElementById("chatInput").focus();
}

function newChat(){
  document.getElementById("messages").innerHTML='<div class="msg ai">New chat started. How can I help you?</div>';
}

function chatKey(e){
  if(e.key==="Enter" && !e.shiftKey){
    e.preventDefault();
    sendChat();
  }
}

function sendChat(){
  const input=document.getElementById("chatInput");
  const text=input.value.trim();
  if(!text)return;
  addMessage(text,"user");
  input.value="";
  setTimeout(()=>{
    let reply="I can help with complaints, campus services, emergency support and general Campus 360 questions.";
    const q=text.toLowerCase();
    if(q.includes("complaint")) reply="You can use Report Complaint to submit a campus issue. The full Flask version can save it to the database.";
    else if(q.includes("emergency")||q.includes("sos")) reply="For an emergency, use the SOS button at the top-right. In India, 112 is the national emergency number.";
    else if(q.includes("password")||q.includes("login")) reply="Use your official @campus.360 account. Student credentials are created by the administrator.";
    addMessage(reply,"ai");
  },400);
}
function addMessage(text,type){
  const box=document.getElementById("messages");
  const div=document.createElement("div");
  div.className="msg "+type;
  div.textContent=text;
  box.appendChild(div);
  box.scrollTop=box.scrollHeight;
}
