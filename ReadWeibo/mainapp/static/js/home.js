function follow_topic(topic_id, u_id) {
  var post_follow_topic = {'t_id': topic_id, 'u_id': u_id};
  $.ajax({
    url: '/follow_topic/',
    type: 'post',
    dataType: 'json',
    data: JSON.stringify(post_follow_topic),
    success: function (follow_success) {
      if (follow_success) {
        //TODO: 位置移动。。。
        $('#topic-' + topic_id.toString() + '-' + u_id.toString()).addClass("unfollow-topic").removeClass("follow-topic").text("取消关注")
      }
    }
  });
  return false;
}

function unfollow_topic(topic_id, u_id) {
  var post_unfollow_topic = {'t_id': topic_id, 'u_id': u_id};
  $.ajax({
    url: '/unfollow_topic/',
    type: 'post',
    dataType: 'json',
    data: JSON.stringify(post_unfollow_topic),
    success: function (unfollow_success) {
      if (unfollow_success) {
        //TODO: 位置移动。。。
        $('#topic-' + topic_id.toString() + '-' + u_id.toString()).addClass("follow-topic").removeClass("unfollow-topic").text("关注")
      }
    }
  });
  return false;
}

function show_more_topics(type, start_idx, count, exclude_user) {
	// alert('show_more_topics:\nstart_idx:' + start_idx.toString() + '\ncount:' + count.toString() + '\nexclude_user:' + exclude_user.toString())
    var post_more_topics = {'type': type, 'start_idx': start_idx, 'count': count, 'exclude_user': exclude_user}
    $.ajax({
	    url: '/show_more_topics/',
	    type: 'post',
	    dataType: 'json',
	    data: JSON.stringify(post_more_topics),
	    success: function (more_topics) {
	      if (more_topics) {
	        if(type=='new'){
	          $('#new-topic-list').append(more_topics)
	          $('#more-new-topic-'+start_idx.toString()).attr('id', 'more-new-topic-' + (start_idx + count).toString())
	        }else{
	        // type==hot
	          $('#other-topic-list').append(more_topics)
  	          $('#more-hot-topic-'+start_idx.toString()).attr('id', 'more-hot-topic-' + (start_idx + count).toString())
	        }
	      }else{
	        alert('只有这么多啦～');
	      }
	    }
    });
  return false;
}

function setting_alert(type, message) {
    $("#setting-alert").append($("<div class='alert alert-" + type + " fade in' data-alert><p> " + message + " </p></div>"));
    $("#setting-alert").delay(2000).fadeOut("slow", function () { $(this).remove(); });
}

$(document).ready(function () {
	
	$(".topic-operation").live('click', function (e) {
		if (!e.target) {
		    return;
		}
		e.preventDefault();
		t_id = parseInt(e.target.id.split("-")[1], 10);
		u_id = parseInt(e.target.id.split("-")[2], 10);
		if(!u_id) {
		    alert('请先登录');
		    //return;
		}
		if(e.target.className.indexOf("unfollow-topic") != -1){
		    unfollow_topic(t_id, u_id);
		}else if(e.target.className.indexOf("follow-topic") != -1){
			follow_topic(t_id, u_id);
		}
	});
   
   $(".more-topic").click(function (e) {
	if (!e.target) {
	    return;
	}
	e.preventDefault();
	type = e.target.id.split("-")[1]
	start_idx = parseInt(e.target.id.split("-")[3], 10);
	count = 5;
	exclude_user = true;
	show_more_topics(type, start_idx, count, exclude_user);
   });
   
   $('#setting-form').submit(function() { // catch the form's submit event
   	
	    $.ajax({ // create an AJAX call...
	        data: $(this).serialize(), // get the form data
	        type: $(this).attr('method'), // GET or POST
	        url: $(this).attr('action'), // the file to call
	        success: function(response) {
	            setting_alert('success', '保存成功!');
	        }
    });
    return false;
});
        
});

