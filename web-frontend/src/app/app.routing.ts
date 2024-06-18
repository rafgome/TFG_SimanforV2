import { Routes } from "@angular/router";

import { FullComponent } from "./layouts/full/full.component";
import { HomeComponent } from "./pages/home/home.component";

export const AppRoutes: Routes = [
  {
    path: "",
    component: FullComponent,
    children: [
      {
        path: "",
        component: HomeComponent,
      },
      {
        path: "",
        loadChildren: () =>
          import("./pages/pages.module").then((m) => m.PagesComponentsModule),
      },
    ],
  },
];
