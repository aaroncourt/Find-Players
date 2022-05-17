function showSearch(ele){
    const searchDiv = document.getElementById(ele).classList;
    const test = document.getElementById(ele)
    console.log(test)
    searchDiv.remove('hidden');
    searchDiv.add('flex');
}

function hideSearch(ele){
    const searchDiv = document.getElementById(ele).classList;
    searchDiv.remove('flex');
    searchDiv.add('hidden');
    console.log(searchDiv)
}
