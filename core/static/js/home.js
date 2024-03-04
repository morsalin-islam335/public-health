
doctors = [ "https://dynaimage.cdn.cnn.com/cnn/digital-images/org/2266330b-cb73-4c38-9621-ea2e7d59c930.jpg", "https://i.postimg.cc/d3SzFmWZ/doctor.jpg", 'https://scx2.b-cdn.net/gfx/news/2021/pfizer-and-biontech-ar.jpg',  "https://i.postimg.cc/d3SzFmWZ/doctor.jpg", 'https://th.bing.com/th/id/R.09bb25615460b342b2559ee85881f9c8?rik=H2E49INrObEYmA&pid=ImgRaw&r=0', 'https://cdn.aarp.net/content/dam/aarp/health/conditions_treatments/2020/10/1140-hepatitis-b.web.jpg', 'https://th.bing.com/th/id/OIP.ToXbNYO825jliCKEyaS1nQHaE8?rs=1&pid=ImgDetMain']


const  loadImage = async () =>{

  for(let i = 0; i < 50; i++){


    const image_side = document.getElementById("img-part")
    image_side.innerHTML = `
    <img id = 'dy-image' style = "width:80%" src="${doctors[0]}" alt="This is image side"></img>
    
    `

    await new Promise(resolve => setTimeout(resolve, 3000)); // image will be change after 3 seconds later

    image_side.innerHTML = `
    <img id = 'dy-image' style = "width:80%" src="${doctors[1]}" alt="This is image side"></img>
    
    `

    await new Promise(resolve => setTimeout(resolve, 3000)); // image will be change after 4 seconds later


    image_side.innerHTML = `
    <img id = 'dy-image' style = "width:80%" src="${doctors[2]}" alt="This is image side"></img>
    
    `

    await new Promise(resolve => setTimeout(resolve, 3000)); // image will be change after 4 seconds later


    image_side.innerHTML = `
    <img id = 'dy-image' style = "width:80%" src="${doctors[3]}" alt="This is image side"></img>
    
    `

    await new Promise(resolve => setTimeout(resolve, 4000)); // image will be change after 4 seconds later

    
    image_side.innerHTML = `
    <img id = 'dy-image' style = "width:80%" src="${doctors[4]}" alt="This is image side"></img>
    
    `

    await new Promise(resolve => setTimeout(resolve, 4000)); // image will be change after 4 seconds later

    
    image_side.innerHTML = `
    <img id = 'dy-image' style = "width:80%" src="${doctors[5]}" alt="This is image side"></img>
    
    `

    await new Promise(resolve => setTimeout(resolve, 4000)); // image will be change after 4 seconds later

    
    image_side.innerHTML = `
    <img id = 'dy-image' style = "width:80%" src="${doctors[6]}" alt="This is image side"></img>
    
    `

    await new Promise(resolve => setTimeout(resolve, 4000)); // image will be change after 4 seconds later

    
}};

loadImage()



const imgPart = () =>{
  const img_side = document.getElementById("dy-image")
  img_side.style.width = '90%'
}

// document.getElementById('img-part')


const resizeImage = () => {
  const img_side = document.getElementById("dy-image")
  img_side.style.width = '80%';
}

