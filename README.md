# Audio Loader - Pack Database
The official pack database for SDH-AudioLoader, an audio loader for the Steam Deck.

# Creating a pack for the Audio Loader
Development for the Audio Loader is intended to be as simple as possible. That being said, we understand not everyone understands how to edit audio and JSON files. If you have any suggestions for how we can make this guide easier to understand, please feel free to create an issue.

## Prerequisites
- Audio Loader installed on a Steam Deck (or compatible device running the Steam Deck UI)
- Basic audio editing and JSON knowledge
- Audio files to use in a pack
- (Optional) SSH enabled on your Steam Deck
- (Optional) An FTP or SSH client on another computer

## Setting up SSH (optional)
This is an optional step that will allow you to easily manage your pack's files remotely. Please follow one of the guides below to learn how to use SSH with your Steam Deck.
- [Enabling SSH Server on a Steam Deck](https://shendrick.net/Gaming/2022/05/30/sshonsteamdeck.html), Seth Hendrick

## Creating a template
To start, create a GitHub repository with a folder inside named after your pack. You can do this by clicking the + at the top-right of GitHub and selecting "New repository". Next, create a file titled `pack.json` inside of the folder with the following contents.
```json
{
  "name": "Pack Name",
  "description": "Use this field to describe the pack.",
  "author": "GitHubUsername",
  "version": "v1.0",
  "manifest_version": 1,
  "music": false,
  "ignore": []
}
```

## Editing pack.json
Please follow these guidelines when changing variables inside your manifest.
- `name` - This is a permanent name that should describe your pack or allude to how it sounds like. For example, calling a science-fiction pack and calling it "Medieval" will likely get denied.
- `description` - This should describe your pack at a basic level. Try to include where you obtained your audio from or the feeling it conveys.
- `author` -  This can be any name. We recommend using your GitHub username so users can easily report an issue if needed.
- `version` - This should follow the format of `v{MAJOR}.{MINOR}`. Major updates are usually new inclusions to the pack that help complete it. Minor updates are usually updates to poor or unintentionally missing audio or adding support for a new version of SteamOS.
- `manifest_version` - This should always reflect the latest manifest version available in this guide. Newer manifest versions provide additional features only available on newer installations. Make sure to check this README for a guide on updating versions.
- `music` - This determines whether your pack displays as music or Steam UI sound replacements.
- `ignore` - This controls which Steam UI sound files will not be customized if creating a sound pack. This is necessary if not replacing all sounds.

## Adding sound files
This is where the guide will split in two. If you are looking to add background music to the Steam UI, please read the **Music packs** section. If you are looking to replace existing Steam UI sounds, please read the **Sound packs** section.

### Music packs
Music packs are background tracks for the Steam UI. Whenever a user does not have an application running, the active music pack will play indefinitely until an application is launched.

When creating a music pack, the first thing you should always have in mind is that this is a background track, not a general music player. Consider using ambience and instrumental songs rather than heavy hitting songs or anything with lyrics. Exceptions can be made but they shouldn't be expected.

Once you have found a song that you want to use for your pack, make the following changes to your `pack.json`.
- Change `name` to the exact song name. Don't use descriptions like "This Character's Theme".
- Use `description` to credit the source. You can also list where it appears in a game if applicable (ex. Dr. Maruki's theme from...).
- Make sure `music` is set to true.

Next, find an audio file for the song you would like to use. Using an audio editing program (ex. Audacity), do the following.
- Make the song loop as seamlessly as possible. If you can't do this, please merge any pull requests doing so in your repo.
- Decrease the volume of the song by 10dB. In Audacity, select Effect and Amplify. Enter -10 as the New Peak Amplitude.
  - Keep in mind that your music pack will be denied if sound packs cannot be heard over it.
- Save your song as `menu_music.mp3` in your pack directory. In Audacity, select File, Export, and Export as MP3.

When uploading your music pack, please try to use the cover art for the album you retrieved the song from (more info about this below). For a video game, this should be the cover of the original soundtrack and not the box art for the game itself.

### Sound packs
To start, you will need to find the folder containing the Steam UI sounds. This can be found at `/home/deck/.local/share/Steam/steamui/sounds` on your Steam Deck. [If you have run the Steam Deck UI on another device](https://www.youtube.com/watch?v=1IAbZte8e7E), you can find the sounds at `{STEAM_INSTALLATION}/steamui/sounds`. **DO NOT MODIFY THESE FILES UNDER ANY CIRCUMSTANCE.** Modifying your Steam files is destructive and could lead to problems in the future. Using Audio Loader to manage your sound replacements is the safest way to avoid any potential issues.

Create a list of these file names as you will need to create a replacement or add an entry to your ignore array for all of them. For your convenience, an array of all file names is available below if you prefer to work from the bottom up.
```json
"ignore": [
  "bumper_end.wav",
  "confirmation_negative.wav",
  "confirmation_positive.wav",
  "deck_ui_achievement_toast.wav",
  "deck_ui_bumper_end_02.wav",
  "deck_ui_default_activation.wav",
  "deck_ui_hide_modal.wav",
  "deck_ui_into_game_detail.wav",
  "deck_ui_launch_game.wav",
  "deck_ui_message_toast.wav",
  "deck_ui_misc_01.wav",
  "deck_ui_misc_08.wav",
  "deck_ui_misc_10.wav",
  "deck_ui_navigation.wav",
  "deck_ui_out_of_game_detail.wav",
  "deck_ui_show_modal.wav",
  "deck_ui_side_menu_fly_in.wav",
  "deck_ui_side_menu_fly_out.wav",
  "deck_ui_slider_down.wav",
  "deck_ui_slider_up.wav",
  "deck_ui_switch_toggle_off.wav",
  "deck_ui_switch_toggle_on.wav",
  "deck_ui_tab_transition_01.wav",
  "deck_ui_tile_scroll.wav",
  "deck_ui_toast.wav",
  "deck_ui_typing.wav",
  "deck_ui_volume.wav",
  "pop_sound.wav",
  "steam_at_mention.m4a",
  "steam_chatroom_notification.m4a",
  "ui_steam_message_old_smooth.m4a",
  "ui_steam_smoother_friend_join.m4a",
  "ui_steam_smoother_friend_online.m4a"
]
```

To replace a sound file, remove its entry from the above array and place a sound file with the exact file name (including file type) inside of your pack folder. Below is a list of what each sound file is believed to mean.
- `bumper_end.wav` - Unknown or unused.
- `confirmation_negative.wav` - Unknown or unused.
- `confirmation_positive.wav` - Unknown or unused.
- `deck_ui_achievement_toast.wav` - Played when a user unlocks an achievement in a Steam game.
- `deck_ui_bumper_end_02.wav` - Played when attempting to navigate and being unable to move further.
- `deck_ui_default_activation.wav` - Played when selecting most interactable objects.
- `deck_ui_hide_modal.wav` - Played when exiting most pop-ups.
- `deck_ui_into_game_detail.wav` - Played when opening a game's details page.
- `deck_ui_launch_game.wav` - Played when launching a game.
- `deck_ui_message_toast.wav` - Unknown or unused.
- `deck_ui_misc_01.wav` - Unknown or unused.
- `deck_ui_misc_08.wav` - Unknown or unused.
- `deck_ui_misc_10.wav` - Played when navigating through most areas.
- `deck_ui_navigation.wav` - Played when navigating through specific areas (ex. Settings).
- `deck_ui_out_of_game_detail.wav` - Played when exiting a game's details page.
- `deck_ui_show_modal.wav` - Played when a pop-up appears.
- `deck_ui_side_menu_fly_in.wav` - Played when opening the Steam or Quick Access menus.
- `deck_ui_side_menu_fly_out.wav` - Played when exiting the Steam or Quick Access menus.
- `deck_ui_slider_down.wav` - Played when decreasing a slider.
- `deck_ui_slider_up.wav` - Played when increasing a slider.
- `deck_ui_switch_toggle_off.wav` - Played when toggling off a toggle.
- `deck_ui_switch_toggle_on.wav` - Played when toggling on a toggle.
- `deck_ui_tab_transition_01.wav` - Played when switching between tabs (ex. Library views).
- `deck_ui_tile_scroll.wav` - Unknown or unused.
- `deck_ui_toast.wav` - Played when a toast appears at the bottom-right corner of the UI.
- `deck_ui_typing.wav` - Played when typing on the keyboard.
- `deck_ui_volume.wav` - Played when confirming the volume setting in Settings.
- `pop_sound.wav` - Unknown or unused.
- `steam_at_mention.m4a` - Unknown or unused.
- `steam_chatroom_notification.m4a` - Unknown or unused.
- `ui_steam_message_old_smooth.m4a` - Played when receiving a chat message.
- `ui_steam_smoother_friend_join.m4a` - Unknown or unused.
- `ui_steam_smoother_friend_online.m4a` - Unknown or unused.

## Testing your pack
Once you have completed creating your pack, upload the folder containing it to the `/home/deck/homebrew/sounds` folder. If the sounds folder does not exist, you may not have the Audio Loader plugin properly installed. Depending on the type of pack you created, you should be able to find it in the music or sounds dropdowns. Select your pack and test it by either testing the functionality of each sound or using the [Decky Playground Plugin](https://github.com/SteamDeckHomebrew/decky-playground).

# Uploading a pack to the Pack Browser
Uploading your pack requires some basic Git knowledge. If you have trouble understanding the instructions below, feel free to reach out to us or another developer familiar with Git for support.
1. Create a fork of this repository. You can do this using the Fork button at the top-right corner.
1. (Optional) Create and upload a square JPG preview image in `/images/{AUTHOR}`.
1. Create and upload a JSON file in `/packs` titled `{AUTHOR}-{PACK_NAME}.json` that follows this template.
```json
{
  "repo_url": "https://github.com/AuthorGoesHere/RepoNameGoesHere",
  "repo_subpath": "FolderWherePackIsGoesHere",
  "repo_commit": "a1b2c3",
  "preview_image_path": "images/{AUTHOR}/{IMAGE_NAME}.jpg"
}
```
4. (Optional) Test your pack submission by running `py main.py` in the repository folder.
    - Python and the Git CLI need to be installed.
    - If you are missing Python libraries, run `pip install -r requirements.txt`.
    - If the script throws no exceptions, you are ready to commit.
1. Commit your changes and repeat for as many packs as you plan to upload.
1. Create a pull request from your fork to the main repository.

# Support
If you need any help creating or submitting a pack, please use [the Steam Deck Homebrew Discord server](https://discord.gg/ZU74G2NJzk). Please use the Audio Loader Support thread in the #support-plugins channel.
