let searchButton=  document.querySelector("#search")

searchButton.addEventListener("click", ()=>{
    console.log("button pressed")
    sendApiRequest()
})

   async function sendApiRequest(){
    let API_KEY = "SwegvFQemHFTKbGbER9TZzBEPAnZdBidIgwvFFC7"
    let response = await fetch(`https://api.nasa.gov/planetary/apod?api_key=${API_KEY}`);
    console.log(response)
    let data= await response.json()
    console.log(data)
    useApiData(data)
}


function useApiData(data){
document.querySelector("#content").innerHTML += data.explanation
document.querySelector("#content").innerHTML += `<img src="${data.url}">`

}