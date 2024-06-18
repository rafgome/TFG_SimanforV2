import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'cutter'
})
export class CutterPipe implements PipeTransform {

  transform(value: string): string {
    if (value.length >= 15) {
      value = value.substr(0, 15) + '...';
    }
    return value;
  }
}
