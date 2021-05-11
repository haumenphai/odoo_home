fetch('https://api.db-ip.com/v2/free/self')
.then(res => res.text())
.then(data => {
    console.log(data)
    alert(data)
});