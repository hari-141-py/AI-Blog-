
// Blog Generator 
document.getElementById('generateBlogButton').addEventListener('click', async (event) => {
    event.preventDefault(); // Prevent form submission

    const youtubeLink = document.getElementById('youtubeLink').value.trim();
    const blogContent = document.getElementById('blogContent');
    const loadingCircle = document.getElementById('loadingCircle');

    if (!youtubeLink) {
        alert("Please enter a valid YouTube link.");
        return;
    }

    // Show loading animation properly
    loadingCircle.style.display = 'flex';
    loadingCircle.style.opacity = '1';  // Ensures it's visible
    blogContent.innerHTML = ''; // Clear previous content

    try {
        const response = await fetch('/generate_blog/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ link: youtubeLink })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || `HTTP Error: ${response.status}`);
        }

        blogContent.innerHTML = data.content;
    } 
    catch (error) {
        console.error("Error occurred:", error);
        blogContent.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    }
    finally {
        // Hide loading animation after request completes
        setTimeout(() => {
            loadingCircle.style.opacity = '0';
            setTimeout(() => {
                loadingCircle.style.display = 'none';  // Hide fully after fade out
            }, 300); // Delay to match fade-out effect
        }, 300);
    }
});




// document.getElementById('generateBlogButton').addEventListener('click', async (event) => {
//     event.preventDefault(); // Prevents page reload
//     document.getElementById('loadingCircle').style.display = 'block';
// });


// custom cursor
var main = document.querySelector("body")  // i have changed "#main" to "body" if the below code of image want to work change it back to "#main"
var cursor = document.querySelector("#cursor")
var image = document.querySelector("#image")

// This happens when mouse moves around the div main
main.addEventListener("mousemove",function(dets){
    gsap.to(cursor,{
        x:dets.x,
        y:dets.y,
        duration:1,
        ease: "back.out(3)",
    })
})



gsap.from(".navv",{
    y:30,
    delay:1,
    opacity:"0",
    stagger:-0.5,
})
gsap.from(".intro h1",{
    delay:1.8,
    opacity:"0",
    stagger:-0.5,
})
gsap.from(".intro p",{
    y:30,
    delay:2.5,
    opacity:"0",
    stagger:-0.8,
})
gsap.from(".input,.blog",{
    y:180,
    delay:3,
    duration:1,
    scale:1.8,
    opacity:"0",
})

gsap.from(["#floater1", "#floater2","#floater22", "#floater3"], {
    y: -50, // Change value based on need
    delay: 2,
    duration: 2,
    opacity: 0,
});


// Interactive guitar line

const path = `M 50 100 Q 500 100 1490 100`;

// Function to add interactivity to a specific string
function makeInteractive(selector) {
    const string = document.querySelector(selector);
    let isInside = false;

    string.addEventListener("mouseenter", () => {
        isInside = true;
    });

    string.addEventListener("mousemove", function (dets) {
        if (isInside) {
            gsap.to(`${selector} svg path`, {
                attr: { d: `M 50 100 Q ${dets.offsetX} ${dets.offsetY} 1490 100` },
                duration: 0.3,
                ease: "elastic.out(2, 0.1)",
            });
        }
    });

    string.addEventListener("mouseleave", function () {
        isInside = false;
        gsap.to(`${selector} svg path`, {
            attr: { d: path },
            duration: 2.5,
            ease: "elastic.out(1, 0.1)",
        });
    });
}

// Apply interactivity to both strings
makeInteractive(".string1");
makeInteractive(".string2");


// nav relocation
// Select the navbar element
const navbar = document.querySelector(".navv");

// Variable to track the last scroll position
let lastScrollTop = 0;

// Add a scroll event listener
window.addEventListener("scroll", () => {
    // Get the current scroll position
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    // Determine if the user is scrolling down or up
    if (scrollTop > lastScrollTop) {
        // Scrolling down - move the navbar out of view
        gsap.to(navbar, {
            y: "-100%",
            duration: 0.5,
            ease: "power2.out",
        });
    } else {
        // Scrolling up - bring the navbar back into view
        gsap.to(navbar, {
            y: "0%",
            duration: 0.5,
            ease: "power2.out",
        });
    }

    // Update the last scroll position
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // Prevent negative scrolling values
});

document.addEventListener("mousemove", (event) => {
    const mouseX = event.clientX;
    const mouseY = event.clientY;
  
    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;
  
    const deltaX = mouseX - centerX;
    const deltaY = mouseY - centerY;
  
    // Adjust the angle calculation to correct direction
    const angle = (Math.atan2(deltaY, deltaX) * (180 / Math.PI) + 90) - 270;
  
    const pupils = document.querySelectorAll(".line");
    pupils.forEach((pupil) => {
      pupil.style.transform = `rotate(${angle}deg)`;
    });
  });

  gsap.from(".how",{
    y:30,
    delay:0.5,
    opacity:"0",
    stagger:-0.5,
    scrollTrigger:".how"
  })
  gsap.from(".page1 .card",{
    y:30,
    delay:0.8,
    duration:2,
    opacity:"0",
    stagger:-0.5,
    scrollTrigger:".page1 .card"
  })
    gsap.from(".page2",{
    y:80,
    delay:1,
    duration:1.5,
    opacity:"0",
    stagger:-0.5,
    scrollTrigger:".page2"
  })
  gsap.from(".page3",{
    xy:80,
    delay:1,
    duration:1.5,
    opacity:"0",
    stagger:-0.5,
    scrollTrigger:".page3"
  })
  gsap.from("footer",{
    y:80,
    delay:1,
    opacity:"0",
    stagger:-0.5,
    scrollTrigger:".footer"
  })


  const menuButton = document.querySelector(".menu");
  const menu = document.querySelector("#full");
  const menuLinks = document.querySelectorAll("#full a"); // Select all menu links
  const closeButton = document.querySelector("#full i"); // Close button
  
  // Initially hide the close button and menu links
  gsap.set(menu, { opacity: 0, top: "-100vh", backdropFilter: "blur(8px)" });
  gsap.set(menuLinks, { opacity: 0, y: 30 });
  gsap.set(closeButton, { opacity: 0, y: 30 });
  
  // Open menu animation
  menuButton.addEventListener("click", function () {
      gsap.to(menu, {
          duration: 1.2,
          top: 0,
          opacity: 1,
          backdropFilter: "blur(8px)", // Ensures blur remains constant
          ease: "power3.out",
          onStart: () => {
              menu.style.display = "block"; // Ensure it's visible before animating
          },
          onComplete: () => {
              gsap.to(menuLinks, {
                  opacity: 1,
                  y: 0,
                  duration: 0.8,
                  stagger: 0.2,
                  ease: "power3.out",
                  onComplete: () => {
                      gsap.to(closeButton, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" });
                  }
              });
          }
      });
  });
  
  // Close menu on clicking the close icon
  closeButton.addEventListener("click", function () {
      gsap.to(closeButton, { opacity: 0, y: 30, duration: 0.3, ease: "power3.in" });
  
      gsap.to(menuLinks, {
          opacity: 0,
          y: 30,
          duration: 0.5,
          stagger: 0.1,
          ease: "power3.in",
          onComplete: () => {
              gsap.to(menu, {
                  duration: 0.5,
                  opacity: 0,
                  top: "-100vh",
                  backdropFilter: "blur(8px)",
                  ease: "power3.in",
                  onComplete: () => {
                      menu.style.display = "none"; // Hide menu after animation ends
                  }
              });
          }
      });
  });
  
  // Close menu when a menu link is clicked (even for external links or section links)
  menuLinks.forEach(link => {
      link.addEventListener("click", function (e) {
          // Prevent default behavior for internal links (section navigation)
          e.preventDefault();
  
          // Get the target section or page
          const target = link.getAttribute("href");
  
          // Close the menu
          gsap.to(closeButton, { opacity: 0, y: 30, duration: 0.3, ease: "power3.in" });
  
          gsap.to(menuLinks, {
              opacity: 0,
              y: 30,
              duration: 0.5,
              stagger: 0.1,
              ease: "power3.in",
              onComplete: () => {
                  gsap.to(menu, {
                      duration: 0.5,
                      opacity: 0,
                      top: "-100vh",
                      backdropFilter: "blur(8px)",
                      ease: "power3.in",
                      onComplete: () => {
                          menu.style.display = "none"; // Hide menu after animation ends
                          
                          // If it's a section within the same page, scroll to it
                          if (target.startsWith('#')) {
                              const targetElement = document.querySelector(target);
                              if (targetElement) {
                                  targetElement.scrollIntoView({ behavior: "smooth" });
                              }
                          } else {
                              // If it's an external or different page, just follow the link
                              window.location.href = target;
                          }
                      }
                  });
              }
          });
      });
  });
  