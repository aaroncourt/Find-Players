function showSearch(ele){
    console.log(ele)
    const searchDiv = document.getElementById(ele).classList;
    searchDiv.remove('hidden')
    searchDiv.add('flex')
}

function hideSearch(ele){
    const searchDiv = document.getElementById(ele).classList;
    searchDiv.remove('flex')
    searchDiv.add('hidden')
}