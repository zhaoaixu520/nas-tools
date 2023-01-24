import { LitElement } from "./lit-core.min.js";

export class CustomElement extends LitElement {

  // 兼容前进后退时重载
  connectedCallback() {
    super.connectedCallback();
    this.innerHTML = "";
  }

  // 过滤空字符
  attributeChangedCallback(name, oldValue, newValue) {
    super.attributeChangedCallback(name, oldValue, Golbal.repNull(newValue));
  }

  // 不使用影子dom
  createRenderRoot() {
    return this;
  }

}

export class Golbal {

  // 没有图片时
  static noImage = "../static/img/no-image.png";
  static noImage_person = "../static/img/person.png";

  // 转换传值的空字符情况
  static repNull(value) {
    if (!value || value == "None" || value == "null" || value == "undefined") {
      return "";
    } else {
      return value;
    }
  }

  // 是否触摸屏设备
  static is_touch_device() {
    return 'ontouchstart' in window;
  }

  static lit_love_click(title, year, page_type, tmdb_id, fav, remove_func, add_func) {
    if (fav == "1"){
      show_ask_modal("是否确定将 " + title + " 从订阅中移除？", function () {
        hide_ask_modal();
        remove_rss_media(title, year, page_type, "", "", tmdb_id, remove_func);
      });
    } else {
      show_ask_modal("是否确定订阅： " + title + "？", function () {
        hide_ask_modal();
        let tid;
        let did;
        if (tmdb_id && tmdb_id.startsWith("DB:")) {
          did = tmdb_id.replace("DB:", "");
          tid = "";
        } else if (isNaN(tmdb_id)) {
          did = "";
          tid = "";
        } else {
          did = "";
          tid = tmdb_id;
        }
        if (!tid || page_type == "MOV") {
          add_rss_media(title, year, page_type, tid, did, "", "", add_func);
        } else {
          ajax_post("get_tvseason_list", { tmdbid: tid }, function (ret) {
            if (ret.seasons.length === 1) {
              add_rss_media(title, year, "TV", tid, did, "", "", add_func);
            } else if (ret.seasons.length > 1) {
              show_rss_seasons_modal(title, year, "TV", tid, did, ret.seasons, add_func);
            } else {
              show_fail_modal(title + " 添加RSS订阅失败：未查询到季信息！");
            }
          });
        }
      });
    }
  }

}