const videoLoader = document.querySelectorAll('.play-video')
let nextToken = ''
const contentDiv = document.querySelector('.vids')

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting){
            let videoId = document.querySelector('.play-video').id
            fetch(`http://localhost:5000/similar_videos?video_id=${videoId}&next_token=${nextToken}`,{
            method: 'GET',
        }).then(
            response => response.json()
        ).then(
            response => {
                console.log(JSON.stringify(response))
                videos = response['videos']
                nextToken = response['next_token']
                loadSimilarVideos(videos)
            }
        )
            }
        })
},
{
    threshold: 0.2
}
)

for(let i = 0; i < videoLoader.length; i++){
    const elements = videoLoader[i];

    observer.observe(elements);
}

const loadSimilarVideos = (videos) => {
    videos.forEach(video => {
        const vidList = document.createElement('div')
        vidList.classList.add('side-video-list')

        const channelBanner = document.createElement('img')
        channelBanner.src = video['video_thumbnail']
        const video_link = document.createElement('a')
        video_link.classList.add('small-thumbnail')
        video_link.appendChild(channelBanner)

        const videoInfo = document.createElement('div')
        videoInfo.classList.add('vid-info')

        const videoTitle = document.createElement('a')
        videoTitle.textContent = video['video_title']
        videoInfo.appendChild(videoTitle)

        const channelTitle = document.createElement('p')
        channelTitle.textContent = video['channel_title']
        videoInfo.appendChild(channelTitle)

        const channelStats = document.createElement('p')
        channelStats.textContent = '15k Views'
        videoInfo.appendChild(channelStats)
        
        vidList.appendChild(video_link)
        vidList.appendChild(videoInfo)

        contentDiv.appendChild(vidList)
    })
}