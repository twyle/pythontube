const profileDropDownBtn = document.querySelector('.nav-right')
const profileDropDown = document.querySelector('.context-menu')
const homeLoader = document.querySelectorAll('.home')
const contentDiv = document.querySelector('.list-container')
let nextToken = '';

profileDropDownBtn.addEventListener('click', () => {
    profileDropDown.style.display = 'block'
    setTimeout(() => {
        profileDropDown.style.display = 'none'
    }, 2000)
})

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting){
            fetch(`http://localhost:5000/load_videos?next_token=${nextToken}`,{
            method: 'GET',
        }).then(
            response => response.json()
        ).then(
            response => {
                // console.log(JSON.stringify(response))
                videos = response['videos']
                nextToken = response['next_token']
                loadMoreVideos(videos)
            }
        )
            }
        })
},
{
    threshold: 0.2
}
)

for(let i = 0; i < homeLoader.length; i++){
    const elements = homeLoader[i];

    observer.observe(elements);
}

const loadMoreVideos = (videos) => {
    videos.forEach(video => {
        const vidList = document.createElement('div')
        vidList.classList.add('vid-list')

        const channelBanner = document.createElement('img')
        channelBanner.src = video['video_thumbnail']
        channelBanner.classList.add('thumbnail')
        const video_link = document.createElement('a')
        video_link.appendChild(channelBanner)

        const flexDiv = document.createElement('div')
        flexDiv.classList.add('flex-div')
        const userProfile = document.createElement('img')
        userProfile.src = video['channel_thumbnail']
        flexDiv.appendChild(userProfile)

        const videoInfo = document.createElement('div')
        videoInfo.classList.add('vid-info')

        const videoTitle = document.createElement('a')
        videoTitle.textContent = video['video_title']
        videoInfo.appendChild(videoTitle)

        const channelTitle = document.createElement('p')
        channelTitle.textContent = video['channel_title']
        videoInfo.appendChild(channelTitle)

        const channelStats = document.createElement('p')
        channelStats.textContent = `${video['view_count']} Views &bull; 2 days`
        videoInfo.appendChild(channelStats)

        flexDiv.appendChild(videoInfo)
        
        vidList.appendChild(video_link)
        vidList.appendChild(flexDiv)

        contentDiv.appendChild(vidList)
    })
}