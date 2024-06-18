import { Component, Inject, Input, OnInit, ElementRef, ViewChild } from "@angular/core";
import { MatDialogRef } from "@angular/material";
import { ScenarioService } from "../../../_services/scenario.service";

@Component({
  selector: "app-results",
  templateUrl: "./results.component.html",
  styleUrls: ["./results.component.css"],
})
export class ResultsComponent implements OnInit {
  @Input() dataModel: any;
  fileName: string;
  
  public loading = false;
  adBlockerEnabled: boolean;
  @ViewChild("wrapadtest") adElementView: ElementRef;

  constructor(
    public dialogRef: MatDialogRef<ResultsComponent>,
    private scenarioService: ScenarioService
  ) {}

  ngAfterViewInit(): void {
    const adHeight = this.adElementView.nativeElement.offsetHeight;
    this.adBlockerEnabled = adHeight > 0 ? false : true;
  }

  ngOnInit(): void {
    this.fileName = this.dataModel.outputFile;
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  download(_id): void {
    this.loading = true;

    this.scenarioService.downloadResult(_id).subscribe(
      (data) => {
        this.loading = false;
        this.downLoadFile(data, "application/zip");
        console.log(data);
      },
      (error) => {
        this.loading = false;
        console.log(error);
      }
    );
  }

  downLoadFile(data: any, type: string) {
    let blob = new Blob([data], { type: type });
    let url = window.URL.createObjectURL(blob);
    let pwa = window.open(url);
    if (
      !pwa ||
      pwa.closed ||
      typeof pwa.closed == "undefined" ||
      this.adBlockerEnabled
    ) {
      alert(
        "Pop-up blocker and Ad blocker can block some features of this webpage. Please disable them and try again."
      );
    }
  }

  connectRShiny(): void {
    window.open('http://localhost:8787/', '_blank');
    // window.open('https://www.simanfor.es/rstudio', '_blank');
  }
}


