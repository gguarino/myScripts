#backup

This is a simple script to backup a wordpress website to a google drive directory using [rclone](https://rclone.org/)

To configure rclone

`rclone config`

This will guide you through an interactive setup process:

`No remotes found - make a new one
 n) New remote
 r) Rename remote
 c) Copy remote
 s) Set configuration password
 q) Quit config
 n/r/c/s/q> n
 name> remote
 Type of storage to configure.
 Choose a number from below, or type in your own value
 [snip]
 XX / Google Drive
    \ "drive"
 [snip]
 Storage> drive
 Google Application Client Id - leave blank normally.
 client_id>
 Google Application Client Secret - leave blank normally.
 client_secret>
 Scope that rclone should use when requesting access from drive.
 Choose a number from below, or type in your own value
  1 / Full access all files, excluding Application Data Folder.
    \ "drive"
  2 / Read-only access to file metadata and file contents.
    \ "drive.readonly"
    / Access to files created by rclone only.
  3 | These are visible in the drive website.
    | File authorization is revoked when the user deauthorizes the app.
    \ "drive.file"
    / Allows read and write access to the Application Data folder.
  4 | This is not visible in the drive website.
    \ "drive.appfolder"
    / Allows read-only access to file metadata but
  5 | does not allow any access to read or download file content.
    \ "drive.metadata.readonly"
 scope> 1
 ID of the root folder - leave blank normally.  Fill in to access "Computers" folders. (see docs).
 root_folder_id> 
 Service Account Credentials JSON file path - needed only if you want use SA instead of interactive login.
 service_account_file>
 Remote config
 Use auto config?
  * Say Y if not sure
  * Say N if you are working on a remote or headless machine or Y didn't work
 y) Yes
 n) No
 y/n> y
 If your browser doesn't open automatically go to the following link: http://127.0.0.1:53682/auth
 Log in and authorize rclone for access
 Waiting for code...
 Got code
 Configure this as a team drive?
 y) Yes
 n) No
 y/n> n
 --------------------
 [remote]
 client_id = 
 client_secret = 
 scope = drive
 root_folder_id = 
 service_account_file =
 token = {"access_token":"XXX","token_type":"Bearer","refresh_token":"XXX","expiry":"2014-03-16T13:57:58.955387075Z"}
 --------------------
 y) Yes this is OK
 e) Edit this remote
 d) Delete this remote
 y/e/d> y`


You can then use it like this,

List directories in top level of your drive

`rclone lsd remote:`