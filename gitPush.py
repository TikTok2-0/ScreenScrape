from git import Repo

repoPath = r'/home/kfuadmin/Downloads/ScreenScrape'
messageCommit = 'Update News'

username = "y1music"
password = "6ce1d3eef6e7ab177a641dda5966f5ef467c4236"
remote = f"https://{username}:{password}@github.com/TikTok2-0/ScreenScrape.git"

def git_push():

	repo = Repo(repoPath)
	repo.git.add(update=True)   
	repo.index.commit(messageCommit)
	origin = repo.remote(name='origin')
	origin.push() 

git_push()
