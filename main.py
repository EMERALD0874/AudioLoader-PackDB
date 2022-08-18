from os import listdir
from os.path import isfile, join
import json, subprocess, tempfile, os, time, uuid, boto3, binascii, hashlib, sys, shutil, requests
from botocore.config import Config
from dateutil.parser import parse

if (os.path.exists("zips")):
    shutil.rmtree("zips")

os.mkdir("zips")

files = [f for f in listdir("./packs") if isfile(join("./packs", f)) and f.endswith(".json")]

UPLOAD_FILES = "upload" in sys.argv
FORCE_REFRESH = "force" in sys.argv

# Stolen from https://github.com/suchmememanyskill/CssLoader-ThemeDb/blob/main/main.py who stole from https://github.com/backblaze-b2-samples/b2-python-s3-sample/blob/main/sample.py
class B2Bucket():
    def __init__(self, b2Connection, bucket):
        self.resource = b2Connection
        self.bucket = bucket
        self.loadFiles()
        pass

    def loadFiles(self):
        self.files = [x for x in self.bucket.objects.all()]
    
    def fileExists(self, fileName : str) -> bool:
        for x in self.files:
            if x.key == fileName:
                return True
        return False

    def getFileUrl(self, fileName : str) -> str:
        for x in self.files:
            if x.key == fileName:
                return f"{self.resource.ENDPOINT}/{x.bucket_name}/{x.key}"

        return None
    
    def upload(self, path : str):
        filename = os.path.basename(path)
        self.bucket.upload_file(path, filename)

class B2Connection():
    def __init__(self):
        self.ENDPOINT = os.getenv("SECRET_ENDPOINT")
        self.KEYID = os.getenv("SECRET_KEYID")
        self.APPLICATIONKEY = os.getenv("SECRET_APPLICATIONKEY")
        self.resource = boto3.resource(service_name='s3',
                        endpoint_url=self.ENDPOINT,                # Backblaze endpoint
                        aws_access_key_id=self.KEYID,              # Backblaze keyID
                        aws_secret_access_key=self.APPLICATIONKEY, # Backblaze applicationKey
                        config = Config(
                            signature_version='s3v4',
                        ))
    
    def getBucket(self, bucketName : str) -> B2Bucket:
        bucket = self.resource.Bucket(bucketName)
        return B2Bucket(self, bucket)


b2Connection = None
b2PackBucket = None

if (UPLOAD_FILES):
    print("Connecting to backblaze...")
    b2Connection = B2Connection()
    b2PackBucket = b2Connection.getBucket("AudioLoaderPacks")

class MegaJson():
    def __init__(self):
        self.megaJson = requests.get("https://github.com/EMERALD0874/AudioLoader-PackDB/releases/download/1.0.0/packs.json").json()

    def getMegaJsonEntry(self, packId : str) -> dict:
        for x in self.megaJson:
            if (packId == x["id"]):
                return x
        return None


print("Getting megajson...")
megaJson = MegaJson()

class RepoReference:
    def __init__(self, json : dict, path : str):
        self.path = path
        self.repoUrl = json["repo_url"] if "repo_url" in json else None
        self.repoSubpath = json["repo_subpath"] if "repo_subpath" in json else "."
        self.repoCommit = json["repo_commit"] if "repo_commit" in json else None
        self.previewImage = ""
        self.previewImagePath = json["preview_image_path"] if "preview_image_path" in json else "images/default.jpg"
        self.downloadUrl = ""
        self.repo = None
        self.id = binascii.hexlify(hashlib.sha256(f"{self.repoUrl}.{self.repoSubpath}.{self.repoCommit}".encode("utf-8")).digest()).decode("ascii")
        self.megaJsonEntry = None
        self.music = None

        result = subprocess.run(["git", "log", "-1", "--pretty=%ci", path], capture_output=True)
        dateText = result.stdout.decode("utf-8").strip()
        if (dateText == ""):
            # Assume the pack is new. This will get fixed when it's actually committed
            self.lastChanged = ""
        else:
            parsedDate = parse(dateText)
            self.lastChanged = parsedDate.isoformat()

    def verify(self):
        if self.repoUrl is None:
            raise Exception("No repo URL was specified. Please add a link to your repository in your pack.json.")
        
        if self.repoCommit is None:
            raise Exception("No commit was specified. Please specify a commit in your pack.json.")

        if not os.path.exists(self.previewImagePath):
            raise Exception("The preview image does not exist in the pack database repository. Please add the image to the repository.")
        
        self.previewImage = f"https://raw.githubusercontent.com/EMERALD0874/AudioLoader-PackDB/main/{self.previewImagePath}"
    
    def existsInMegaJson(self) -> bool:
        self.megaJsonEntry = megaJson.getMegaJsonEntry(self.id)
        return self.megaJsonEntry != None

    def toDict(self):
        packId = self.id
        downloadUrl = self.downloadUrl
        previewImage = self.previewImage
        name = None
        version = None
        author = None
        lastChanged = self.lastChanged
        repo = self.repoUrl
        manifestVersion = 1
        description = None
        music = None

        if self.repo != None:
            name = self.repo.name
            version = self.repo.version
            author = self.repo.author
            manifestVersion = self.repo.manifestVersion
            description = self.repo.description
            music = self.repo.music

        if self.megaJsonEntry != None:
            def possiblyReturnMegaJsonStuff(attribute : str, original):
                return self.megaJsonEntry[attribute] if attribute in self.megaJsonEntry else original

            packId = possiblyReturnMegaJsonStuff("id", packId)
            downloadUrl = possiblyReturnMegaJsonStuff("download_url", downloadUrl)
            previewImage = possiblyReturnMegaJsonStuff("preview_image", previewImage)
            name = possiblyReturnMegaJsonStuff("name", name)
            version = possiblyReturnMegaJsonStuff("version", version)
            author = possiblyReturnMegaJsonStuff("author", author)
            manifestVersion = possiblyReturnMegaJsonStuff("manifest_version", manifestVersion)
            description = possiblyReturnMegaJsonStuff("description", description)
            music = possiblyReturnMegaJsonStuff("music", music)
        
        return {
            "id": packId,
            "download_url": downloadUrl,
            "preview_image": previewImage,
            "name": name,
            "version": version,
            "author": author,
            "last_changed": lastChanged,
            "source": repo,
            "manifest_version": manifestVersion,
            "description": description,
            "music": music,
        }
    
class Repo:
    def __init__(self, repoReference : RepoReference):
        self.repoReference = repoReference
        self.json = None
        self.name = None
        self.version = None
        self.author = None
        self.music = repoReference.music
        self.hex = self.repoReference.id
        self.packPath = None
        self.repoPath = None
        self.manifestVersion = None
        self.description = None 
    
    def get(self):
        tempDir = tempfile.TemporaryDirectory()
        print(f"Cloning {self.repoReference.repoUrl} into {tempDir.name}...")
        subprocess.run([
            "git",
            "clone",
            self.repoReference.repoUrl,
            tempDir.name
        ], check=True)

        subprocess.run([
            "git",
            "-C",
            tempDir.name,
            "reset",
            "--hard",
            self.repoReference.repoCommit
        ], check=True)

        self.packPath = join(tempDir.name, self.repoReference.repoSubpath)
        packDataPath = join(self.packPath, "pack.json")

        if not os.path.exists(packDataPath):
            raise Exception("pack.json not found!")

        print(f"Reading {packDataPath}")
        with open(packDataPath, "r") as fp:
            data = json.load(fp)
        
        self.read(data)
        self.verify()
        self.zip()

        if (UPLOAD_FILES):
            self.upload()

        print("Cleaning up temp dir...")
        tempDir.cleanup()
    
    def zip(self):
        tempDir = tempfile.TemporaryDirectory()
        print(f"Generating zip...")
        shutil.copytree(self.packPath, join(tempDir.name, self.name))
        shutil.make_archive(join("zips", self.hex), "zip", tempDir.name, ".")
        tempDir.cleanup()

    def upload(self):
        if (b2PackBucket.fileExists(f"{self.hex}.zip")):
            self.repoReference.downloadUrl = b2PackBucket.getFileUrl(f"{self.hex}.zip")
            return

        print("Uploading zip...")
        b2PackBucket.upload(join("zips",f"{self.hex}.zip"))
        b2PackBucket.loadFiles()
        self.repoReference.downloadUrl = b2PackBucket.getFileUrl(f"{self.hex}.zip")

    def read(self, json : dict):
        self.json = json
        self.name = str(json["name"]) if "name" in json else None
        self.version = str(json["version"]) if "version" in json else "v1.0"
        self.author = str(json["author"]) if "author" in json else None # This isn't required by the Audio Loader but should be for the pack store 
        self.music = bool(json["music"]) if "music" in json else self.music
        self.manifestVersion = int(json["manifest_version"]) if "manifest_version" in json else 1
        self.description = str(json["description"]) if "description" in json else ""

    def verify(self):
        if self.json is None:
            raise Exception("No JSON was loaded.")
        
        if self.name is None:
            raise Exception("Pack has no name.")
        
        if self.author is None:
            raise Exception("Pack has no author.")
        
        if (self.music is None):
            raise Exception("Pack does not specify if it's for music or not.")

        ignorePath = join(self.packPath, "ignore.json") if os.path.exists(join(self.packPath, "ignore.json")) else "ignore.json"

        with open(ignorePath, "r") as fp:
            data = json.load(fp)

        if not isinstance(data, list):
            raise Exception("Invalid ignore.json.")

        data.append("ignore.json")
        
        for x in data:
            if os.path.exists(join(self.packPath, x)):
                os.remove(join(self.packPath, x))
                print(f"Removing {x} from pack.")

        expectedFiles = [join(self.packPath, "pack.json")]

        totalSize = 0
        for path, dirs, files in os.walk(self.packPath):
            for file in files:
                filePath = os.path.join(path, file)
                size = os.path.getsize(filePath)
                totalSize += size
                print(f"{x} is {size} bytes.")

        print(f"Total pack size is {totalSize} bytes")

        if (totalSize > 0xA00000): # 10 MB max per pack. This should be a generous amount
            raise Exception("Total pack size exceeds 10 MB. If your pack is larger than this in good faith, please let the maintainer(s) know.")

packs = []

for x in files:
    path = join("./packs", x)
    print(f"Processing {path}...")
    with open(path, "r") as fp:
        data = json.load(fp)

    reference = RepoReference(data, path)
    reference.verify()

    if not FORCE_REFRESH and reference.existsInMegaJson():
        print(f"Skipping {path} as it's up to date")
        packs.append(reference.toDict())
        continue

    repo = Repo(reference)
    repo.get()
    reference.repo = repo

    packs.append(reference.toDict())

print("Verifying there are no identical packs...")
for x in packs:
    if len([y for y in packs if y["name"] == x["name"]]) > 1:
        raise Exception(f"Multiple packs with the same name detected in the repository! Name is '{x['name']}.'")

print("Sorting database...")

def getName(elem):
    return elem["name"]

packs.sort(key=getName)

print("Done! Dumping result.")
with open("packs.json", 'w') as fp:
    json.dump(packs, fp)