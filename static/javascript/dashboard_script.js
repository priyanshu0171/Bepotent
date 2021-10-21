var profileName = document.getElementById("profileName");
profileName.style.display = "none";
function mouseEnter(){
  profileName.style.display = "block";
}
function mouseLeave(){
  profileName.style.display = "none";
}
var sidenavbar = document.getElementById("sideNavigation");
sidenavbar.addEventListener("mouseenter", mouseEnter)
sidenavbar.addEventListener("mouseleave", mouseLeave)
