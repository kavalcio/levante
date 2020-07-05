class RoomHelpers
{
    // TODO: import this file in necessary html files
    static joinRoom(roomKey) {
        $.ajax({
            type: 'POST',
            headers: { "X-CSRFToken": token },
            url: '/join_room/',
            data: {
                roomKey: roomKey,
            },
            success: function (response) {
                if (response !== 'None') {
                    const roomObj = JSON.parse(response);
                    localStorage.setItem('roomId', roomObj[0].pk);
                    localStorage.setItem('isTutorial', roomObj[0].fields.is_tutorial);

                    // Find a new unique user id and add it to the list
                    const userList = JSON.parse(roomObj[0].fields.user_list, true)
                    let userId;
                    $.ajax({
                        type: 'POST',
                        headers: { "X-CSRFToken": token },
                        url: '/add_user_to_room/',
                        data: {
                            room_id: roomObj[0].pk,
                        },
                        success: function (userId) {
                            localStorage.setItem('userId', userId);
                            window.location.pathname = '/rooms/' + roomKey + '/' + userId + '/1/';
                        }
                    });
                } else {
                    alert('room not found');
                }
            },
        });
    }
}