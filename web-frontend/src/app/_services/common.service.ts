import { Injectable } from "@angular/core";

import { BehaviorSubject } from "rxjs/internal/BehaviorSubject";

import { TranslateService } from "@ngx-translate/core";

@Injectable({ providedIn: "root" })
export class CommonService {
  // Loader
  private loaderState = new BehaviorSubject<any>({ state: false, text: "" });
  public loader$ = this.loaderState.asObservable();

  constructor(private translate: TranslateService) {}

  setLoader(state: boolean, text: string = "") {
    this.loaderState.next({
      state: state,
      text: text,
    });
  }

  getDatatableLanguageConfig(translate: TranslateService) {
    let languageConfig = {};

    translate.get("datatable").subscribe((result: any) => {
      languageConfig = {
        processing: result.processing,
        lengthMenu: result.length_menu,
        zeroRecords: result.zero_records,
        emptyTable: result.empty_table,
        info: result.info,
        infoEmpty: result.info_empty,
        infoFiltered: result.info_filtered,
        infoPostFix: result.info_post_fix,
        search: result.search,
        url: result.url,
        thousands: result.thousands,
        loadingRecords: result.loading_records,
        decimal: result.decimal,
        searchPlaceholder: result.search_placeholder,
        paginate: {
          first: result.paginate.first,
          last: result.paginate.last,
          next: result.paginate.next,
          previous: result.paginate.previous,
        },
        aria: {
          sortAscending: result.aria.sort_ascending,
          sortDescending: result.aria.sort_descending,
        },
      };
    });
    return languageConfig;
  }

  objectToFormData(obj: any) {
    const formData = new FormData();

    Object.keys(obj).forEach((prop) => {
      formData.append(prop, obj[prop]);
    });

    return formData;
  }
}
