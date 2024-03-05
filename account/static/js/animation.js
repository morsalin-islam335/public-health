const changeCardSize = (card) => {
  
    // const card = document.getElementById(`card_${id}`)
    card.style.transform = 'scale(1.1)'; // size will be increase fewer
    card.style.transition = 'transform 0.2s'; // time
    
  
  }
  
  
  const resetCardSize = (card) => {
    // const card = document.getElementById(`card_${id}`)
    card.style.transform = 'scale(1)'; // previous size
    card.style.transition = 'transform 0.2s'; // time
    
  }

  

 