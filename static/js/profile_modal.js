const followersModalBtn = document.querySelector('#followersModal');
    
// Add event listeners to the modal buttons
followersModalBtn.addEventListener('shown.bs.modal', function (event) {
  const userId = document.querySelector('#follow-form').dataset.userId;
  axios.get(`/accounts/${userId}/follower/`)
    .then((response) => {
      const followers = response.data.followers;
      const followersList = document.querySelector('#followers-list');
      followersList.className = "row";
      followersList.innerHTML = '';
      followers.forEach(follower => {
        const followerTag = document.createElement('div');
        followerTag.className = "modal--profile--card col-3";
        const followerLink = document.createElement('a');
        followerLink.className = "text-decoration-none link-secondary fw-bold modal--profile--link";
        followerLink.href = `/accounts/profile/${follower.username}`
        const followerImageDiv = document.createElement('div');
        followerImageDiv.className = "profile--image rounded-circle";
        if (follower.profile_image) {
          const followerImage = document.createElement('img');
          followerImage.className = "object-fit-fill profile";
          followerImage.src = follower.image.url;
          followerImage.alt = `${follower.username}'s profile image`;
          followerImageDiv.appendChild(followerImage);
        } else {
          const followerImage = document.createElement('img');
          followerImage.className = "object-fit-fill profile";
          followerImage.src = "/static/image/profile-none.png";
          followerImage.alt = "profile_image_none";
          followerImageDiv.appendChild(followerImage);
        }
        followerLink.appendChild(followerImageDiv);
        const followerName = document.createElement('span');
        followerName.textContent = follower.username;
        followerLink.appendChild(followerName);
        followerTag.appendChild(followerLink);
        followersList.appendChild(followerTag);
      });
    });
})

const form = document.querySelector('#follow-form');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const followersList = document.querySelector('#followers-list');
followersList.className = "row";

form.addEventListener('submit', function(event) {
  event.preventDefault();
  const userId = event.target.dataset.userId;

  axios({
    method: 'post',
    url:`/accounts/${userId}/follow/`,
    headers: {'X-CSRFToken': csrftoken},
  })
    .then((response) => {
      const isFollowed = response.data.is_followed;
      const followBtn = document.querySelector('#follow-form > input[type=submit]');
      if (isFollowed === true) {
        followBtn.value = 'Unfollow';
      } else {
        followBtn.value = 'follow';
      }
      const followingsCounterTag = document.querySelector('#followings-count');
      const followersCounterTag = document.querySelector('#followers-count');
      const followingsCountData = response.data.followings_count;
      const followersCountData = response.data.followers_count;
      followingsCounterTag.textContent = followingsCountData;
      followersCounterTag.textContent = followersCountData;

      // 팔로워 목록 출력
      followers.forEach(follower => {
        const followerTag = document.createElement('div');
        followerTag.classList.add("modal--profile--card", "col-3");
        const followerLink = document.createElement('a');
        followerLink.classList.add("text-decoration-none", "link-secondary", "fw-bold", "modal--profile--link");
        followerLink.href = "#";
        const followerImageDiv = document.createElement('div');
        followerImageDiv.classList.add("profile--image", "rounded-circle");
        if (follower.profile_image) {
          const followerImage = document.createElement('img');
          followerImage.classList.add("object-fit-fill", "profile");
          followerImage.src = follower.image.url;
          followerImage.alt = `${follower.username}'s profile image`;
          followerImageDiv.appendChild(followerImage);
        } else {
          const followerImage = document.createElement('img');
          followerImage.classList.add("object-fit-fill", "profile");
          followerImage.src = "/static/image/profile-none.png";
          followerImage.alt = "profile_image_none";
          followerImageDiv.appendChild(followerImage);
        }
        followerLink.appendChild(followerImageDiv);
        const followerName = document.createElement('span');
        followerName.textContent = follower.username;
        followerLink.appendChild(followerName);
        followerTag.appendChild(followerLink);
        followersList.appendChild(followerTag);
      });
    });
})
