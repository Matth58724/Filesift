<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>FileSift</title>
  <style>
    body {
      background-color: black;
      color: white;
      font-family: sans-serif;
      text-align: center;
      margin: 0;
      padding: 20px;
    }

    h1, h2 {
      color: white;
      margin-top: 40px;
    }

    img, video, iframe {
      margin-top: 20px;
      max-width: 100%;
    }

    /* Small hover for linked screenshot */
    .clickable-thumbnail img {
      border: 2px solid white;
      border-radius: 8px;
      transition: transform 0.2s;
    }

    .clickable-thumbnail img:hover {
      transform: scale(1.10);
    }

    /* Bigger hover for example images */
    .zoom-big {
      transition: transform 0.3s ease-in-out;
    }

    .zoom-big:hover {
      transform: scale(2);
      z-index: 10;
      position: relative;
    }
  </style>
</head>
<body>

  <h1>FileSift</h1>
  <p>A simple language to assist with dealing with or sorting files</p>

  <!-- Clickable image linking to YouTube -->
  <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2xs" target="_blank" class="clickable-thumbnail">
    <img src="docs/assets/Screenshot%202025-05-03%20160247.png" alt="Screenshot" width="200"/>
  </a>

  <h2>Example</h2>
  <img src="docs/assets/Screenshot ProgramflstBefore.png" alt="Before" width="1000" class="zoom-big"/>
  <img src="docs/assets/ProgramflstAfter.png" alt="After" width="1000" class="zoom-big"/>

  <h2>View The Slides</h2>
  <iframe 
    src="https://docs.google.com/presentation/d/e/2PACX-1vQB96CV3sjGqoNEO43GI6c1CjNaFmDfuBdDDmKKqNibkx1i8G_a6knX_OcUBH6iOq7aKQ4kvR42B4E8/pubembed?start=false&loop=false&delayms=30000" 
    frameborder="0" width="960" height="569" 
    allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true">
  </iframe>

  <h2>Video Example</h2>
  <video width="1000" controls>
    <source src="docs/assets/video1440680598 - TrimEND.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>

</body>
</html>
