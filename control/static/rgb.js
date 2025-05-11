
function rgb_toggle(destination) {
    const url = new URL(`${window.location.origin}/rgb/${destination}`);
    fetch(url, {
        method: 'DELETE'
    }).then(response => {
        if (response.ok) {
            if (response.status === 200) {
                showToast(`${destination} turned on`, 'success', 'RGB Control');
            } else if (response.status == 201) {
                showToast(`${destination} turned off`, 'warning', 'RGB Control');
            }
        } else {
            showToast($`Error: ${response.statusText}`)
        }
    })
}

function rgb_set(destination, hex_color) {
    const url = new URL(`${window.location.origin}/rgb/${destination}`);
    fetch(url, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({hex: hex_color })
        }).then(response => {
            if (response.ok) {
                if (response.status === 200) {
                    showToast(`${destination} set to ${hex_color}`, 'success', 'RGB Control');
                }
            } else {
                showToast($`Error: ${response.statusText}`)
            }
            return response.json();
        }).then(data => {
            console.log(data);
        })
    }

function componentToHex(c) {
  var hex = c.toString(16);
  return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
  return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

document.addEventListener('DOMContentLoaded', function() {
    const ids = ['cabin', 'underglow'];
    ids.forEach(id => {
        fetch(`${window.location.origin}/rgb/${id}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            document.getElementById(id).value = rgbToHex(data.last_color.r, data.last_color.g, data.last_color.b);
        });
    });
});
