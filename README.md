# Download YouTube videos from List of Channel

## How to run 
### 1

Make a file called ```config_default.yaml``` and add the following lines

```yaml
api_service_name : "youtube"
api_version : "v3"
api_key : "<your google api key>"
```

Then make another file called `channel_list.txt` with the youtube channel id that you want. Each channel should be on a separate line. For example:

```text
UCM9KEEuzacwVlkt9JfJad7g
UCzolMvIqyoK6hV345m6FjTg
```

You can use `id` or the channel's name.

### 2

run:
```bash
pip install -r requirements.txt
```