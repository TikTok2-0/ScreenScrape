from git import Repo

repoPath = r'/home/kfuadmin/Downloads/ScreenScrape'
messageCommit = 'Update News'

def git_push():
    try:
        repo = Repo(repoPath)
        repo.git.add(update=True)   
        repo.index.commit(messageCommit)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')    

git_push()